#include "mui_list_view.h"
#include "nrf_log.h"
#include "settings.h"

#define LIST_ITEM_HEIGHT 13

#define LIST_ANIM_SHORT_TIME 150
#define LIST_ANIM_LONG_TIME 300

static bool mui_list_view_anim_enabled() { return settings_get_data()->anim_enabled; }

static uint16_t mui_list_view_get_utf8_width(const char *str) { return u8g2_GetUTF8Width(&(mui()->u8g2), str); }

static void mui_list_view_start_text_anim(mui_list_view_t *p_view) {
    if (mui_list_view_anim_enabled()) {
        mui_list_item_t *p_item = mui_list_item_array_get(p_view->items, p_view->focus_index);
        uint32_t focus_text_width = mui_list_view_get_utf8_width(string_get_cstr(p_item->text));
        focus_text_width += mui_list_view_get_utf8_width(string_get_cstr(p_item->sub_text));

        // 화면 너비보다 텍스트가 길 때만 애니메이션을 실행합니다.
        if (focus_text_width > p_view->canvas_width - 13) {
            p_view->text_offset = 0;
            // 스크롤 될 전체 너비 (텍스트 길이 + 반복을 위한 간격)
            int32_t total_scroll_width = focus_text_width + 30; // 30은 텍스트 반복 시 간격

            // 애니메이션 시간과 값 설정
            mui_anim_set_time(&p_view->text_anim, total_scroll_width * 50); // 속도 조절
            mui_anim_set_values(&p_view->text_anim, 0, -total_scroll_width);
            mui_anim_set_auto_restart(&p_view->text_anim, true); // 애니메이션 자동 반복
            // mui_anim_set_start_delay(&p_view->text_anim, 1000); // 존재하지 않는 함수 호출 삭제
            mui_anim_start(&p_view->text_anim);
        } else {
            // 텍스트가 짧으면 애니메이션을 멈추고 오프셋을 초기화합니다.
            p_view->text_offset = 0;
            mui_anim_stop(&p_view->text_anim);
        }
    }
}

static void mui_list_view_start_gap_anim(mui_list_view_t *p_view) {
    if (mui_list_view_anim_enabled()) {
        mui_anim_start(&p_view->gap_anim);
    } else {
        p_view->item_gap = LIST_ITEM_HEIGHT;
    }
}

static void mui_list_view_anim_exec(void *p, int32_t value) {
    mui_list_view_t *p_view = (mui_list_view_t *)p;
    p_view->anim_value = value;
}

static void mui_list_view_text_anim_exec(void *p, int32_t value) {
    mui_list_view_t *p_view = (mui_list_view_t *)p;
    p_view->text_offset = value;
}
static void mui_list_view_gap_anim_exec(void *p, int32_t value) {
    mui_list_view_t *p_view = (mui_list_view_t *)p;
    p_view->item_gap = value;
}

static void mui_list_view_on_draw(mui_view_t *p_view, mui_canvas_t *p_canvas) {
    mui_canvas_set_font(p_canvas, u8g2_font_wqy12_t_gb2312a);
    mui_list_view_t *p_mui_list_view = p_view->user_data;
    p_mui_list_view->canvas_height = p_canvas->height;
    p_mui_list_view->canvas_width = p_canvas->width;

    mui_list_item_array_it_t it;

    mui_list_item_array_it(it, p_mui_list_view->items);

    uint32_t offset_y = p_mui_list_view->scroll_offset;
    if (p_mui_list_view->anim_type == LIST_ANIM_SCROLL) {
        offset_y += p_mui_list_view->anim_value;
    }
    uint32_t index = 0;
    uint32_t focus_y = 0;
    mui_rect_t clip_win_prev;
    mui_rect_t clip_win_cur;
    while (!mui_list_item_array_end_p(it)) {
        mui_list_item_t *item = mui_list_item_array_ref(it);
        int32_t y = index * LIST_ITEM_HEIGHT - offset_y;

        if (y >= -LIST_ITEM_HEIGHT && y <= mui_canvas_get_height(p_canvas)) { // visible object
            uint32_t actual_y = index * p_mui_list_view->item_gap - offset_y;
            mui_canvas_set_font(p_canvas, u8g2_font_siji_t_6x10);
            mui_canvas_draw_glyph(p_canvas, 0, actual_y + 10, item->icon);
            mui_canvas_set_font(p_canvas, u8g2_font_wqy12_t_gb2312a);

            if (index == p_mui_list_view->focus_index) {
                // 선택 상자 그리기
                mui_canvas_set_draw_color(p_canvas, 2); // 반전 색상
                mui_canvas_draw_box(p_canvas, 0, actual_y, mui_canvas_get_width(p_canvas), LIST_ITEM_HEIGHT - 1);
                mui_canvas_set_draw_color(p_canvas, 1); // 원래 색상

                // 클리핑 영역 설정 (아이콘 영역 제외)
                mui_canvas_get_clip_window(p_canvas, &clip_win_prev);
                clip_win_cur.x = 13;
                clip_win_cur.y = actual_y;
                clip_win_cur.h = LIST_ITEM_HEIGHT;
                clip_win_cur.w = mui_canvas_get_width(p_canvas) - 13;
                mui_canvas_set_clip_window(p_canvas, &clip_win_cur);

                uint32_t text_width = mui_list_view_get_utf8_width(string_get_cstr(item->text));

                // 마퀴 효과 적용
                if (text_width > clip_win_cur.w) {
                    const int gap_pixels = 30;
                    mui_canvas_draw_utf8(p_canvas, 13 + p_mui_list_view->text_offset, actual_y + 10,
                                         string_get_cstr(item->text));
                    mui_canvas_draw_utf8(p_canvas, 13 + p_mui_list_view->text_offset + text_width + gap_pixels,
                                         actual_y + 10, string_get_cstr(item->text));
                } else {
                    mui_canvas_draw_utf8(p_canvas, 13, actual_y + 10, string_get_cstr(item->text));
                }

                // 클리핑 영역 복원
                mui_canvas_set_clip_window(p_canvas, &clip_win_prev);
            } else {
                // 선택되지 않은 항목 그리기
                mui_canvas_draw_utf8(p_canvas, 13, actual_y + 10, string_get_cstr(item->text));
            }

            // 부가 텍스트 그리기 (기존 로직 유지)
            if (string_size(item->sub_text) > 0) {
                uint8_t w = mui_canvas_get_utf8_width(p_canvas, string_get_cstr(item->sub_text));
                mui_canvas_draw_utf8(p_canvas, mui_canvas_get_width(p_canvas) - w - 5, actual_y + 10,
                                     string_get_cstr(item->sub_text));
            }
        }

        mui_list_item_array_next(it);
        index++;
    }

    // 스크롤바 그리기
    mui_element_scrollbar(p_canvas, p_mui_list_view->focus_index, mui_list_item_array_size(p_mui_list_view->items));

    if (!p_mui_list_view->first_draw) {
        p_mui_list_view->first_draw = 1;
        mui_list_view_start_text_anim(p_mui_list_view);
        mui_list_view_start_gap_anim(p_mui_list_view);
    }
}

static void mui_list_view_on_input(mui_view_t *p_view, mui_input_event_t *event) {
    mui_list_view_t *p_mui_list_view = p_view->user_data;
    if (event->type == INPUT_TYPE_SHORT || event->type == INPUT_TYPE_REPEAT || event->type == INPUT_TYPE_LONG) {
        switch (event->key) {
        case INPUT_KEY_LEFT:

            if (p_mui_list_view->focus_index > 0) {
                p_mui_list_view->focus_index--;
                uint16_t focus_offset = p_mui_list_view->focus_index * LIST_ITEM_HEIGHT;
                if (focus_offset < p_mui_list_view->scroll_offset) { // scroll up
                    p_mui_list_view->scroll_offset -= LIST_ITEM_HEIGHT;
                    if (mui_list_view_anim_enabled()) {
                        p_mui_list_view->anim_type = LIST_ANIM_SCROLL;
                        p_mui_list_view->anim_value = LIST_ITEM_HEIGHT;
                        mui_anim_set_time(&p_mui_list_view->anim, LIST_ANIM_SHORT_TIME);
                        mui_anim_set_values(&p_mui_list_view->anim, LIST_ITEM_HEIGHT, 0);
                        mui_anim_start(&p_mui_list_view->anim);
                    }
                } else {
                    if (mui_list_view_anim_enabled()) {
                        p_mui_list_view->anim_value = LIST_ITEM_HEIGHT;
                        p_mui_list_view->anim_type = LIST_ANIM_FOCUS;
                        mui_anim_set_time(&p_mui_list_view->anim, LIST_ANIM_SHORT_TIME);
                        mui_anim_set_values(&p_mui_list_view->anim, LIST_ITEM_HEIGHT, 0);
                        mui_anim_start(&p_mui_list_view->anim);
                    }
                }
            } else {
                p_mui_list_view->focus_index = mui_list_item_array_size(p_mui_list_view->items) - 1;
                uint16_t focus_offset = p_mui_list_view->focus_index * LIST_ITEM_HEIGHT;
                uint16_t max_item_num = p_mui_list_view->canvas_height / LIST_ITEM_HEIGHT;
                if (focus_offset >
                    p_mui_list_view->scroll_offset + p_mui_list_view->canvas_height) { // scroll to bottom
                    uint32_t cur_scroll_offset = p_mui_list_view->scroll_offset;
                    p_mui_list_view->scroll_offset = (p_mui_list_view->focus_index - max_item_num) * LIST_ITEM_HEIGHT;
                    uint32_t diff_scroll_offset = p_mui_list_view->scroll_offset - cur_scroll_offset;
                    if (mui_list_view_anim_enabled()) {
                        p_mui_list_view->anim_type = LIST_ANIM_SCROLL;
                        mui_anim_set_time(&p_mui_list_view->anim, LIST_ANIM_LONG_TIME);
                        mui_anim_set_values(&p_mui_list_view->anim, -diff_scroll_offset, 0);
                        mui_anim_start(&p_mui_list_view->anim);
                    }
                } else {
                    if (mui_list_view_anim_enabled()) {
                        p_mui_list_view->anim_value = -p_mui_list_view->focus_index * LIST_ITEM_HEIGHT;
                        p_mui_list_view->anim_type = LIST_ANIM_FOCUS;
                        mui_anim_set_time(&p_mui_list_view->anim, LIST_ANIM_LONG_TIME);
                        mui_anim_set_values(&p_mui_list_view->anim, p_mui_list_view->anim_value, 0);
                        mui_anim_start(&p_mui_list_view->anim);
                    }
                }
            }

            mui_list_view_start_text_anim(p_mui_list_view);

            break;

        case INPUT_KEY_RIGHT:
            if (p_mui_list_view->focus_index < mui_list_item_array_size(p_mui_list_view->items) - 1) {
                p_mui_list_view->focus_index++;
                uint16_t focus_offset = p_mui_list_view->focus_index * LIST_ITEM_HEIGHT;
                if (focus_offset > p_mui_list_view->scroll_offset + p_mui_list_view->canvas_height) { // scroll down
                    p_mui_list_view->scroll_offset += LIST_ITEM_HEIGHT;

                    if (mui_list_view_anim_enabled()) {
                        p_mui_list_view->anim_type = LIST_ANIM_SCROLL;
                        p_mui_list_view->anim_value = -LIST_ITEM_HEIGHT;
                        mui_anim_set_time(&p_mui_list_view->anim, LIST_ANIM_SHORT_TIME);
                        mui_anim_set_values(&p_mui_list_view->anim, -LIST_ITEM_HEIGHT, 0);
                        mui_anim_start(&p_mui_list_view->anim);
                    }
                } else {
                    if (mui_list_view_anim_enabled()) {
                        p_mui_list_view->anim_value = -LIST_ITEM_HEIGHT;
                        p_mui_list_view->anim_type = LIST_ANIM_FOCUS;
                        mui_anim_set_time(&p_mui_list_view->anim, LIST_ANIM_SHORT_TIME);
                        mui_anim_set_values(&p_mui_list_view->anim, -LIST_ITEM_HEIGHT, 0);
                        mui_anim_start(&p_mui_list_view->anim);
                    }
                }
            } else {
                // scroll to first
                uint16_t cur_focus_index = p_mui_list_view->focus_index;
                p_mui_list_view->focus_index = 0;
                if (p_mui_list_view->scroll_offset > 0) {
                    uint32_t cur_scroll_offset = p_mui_list_view->scroll_offset;
                    p_mui_list_view->scroll_offset = 0;

                    if (mui_list_view_anim_enabled()) {
                        p_mui_list_view->anim_value = cur_scroll_offset;
                        p_mui_list_view->anim_type = LIST_ANIM_SCROLL;
                        mui_anim_set_time(&p_mui_list_view->anim, LIST_ANIM_LONG_TIME);
                        mui_anim_set_values(&p_mui_list_view->anim, cur_scroll_offset, 0);
                        mui_anim_start(&p_mui_list_view->anim);
                    }
                } else {
                    if (mui_list_view_anim_enabled()) {
                        p_mui_list_view->anim_value = cur_focus_index * LIST_ITEM_HEIGHT;
                        p_mui_list_view->anim_type = LIST_ANIM_FOCUS;
                        mui_anim_set_time(&p_mui_list_view->anim, LIST_ANIM_LONG_TIME);
                        mui_anim_set_values(&p_mui_list_view->anim, p_mui_list_view->anim_value, 0);
                        mui_anim_start(&p_mui_list_view->anim);
                    }
                }
            }
            mui_list_view_start_text_anim(p_mui_list_view);
            break;

        case INPUT_KEY_CENTER:
            if (p_mui_list_view->selected_cb) {
                if (event->type == INPUT_TYPE_SHORT) {
                    p_mui_list_view->selected_cb(
                        MUI_LIST_VIEW_EVENT_SELECTED, p_mui_list_view,
                        mui_list_item_array_get(p_mui_list_view->items, p_mui_list_view->focus_index));
                } else if (event->type == INPUT_TYPE_LONG) {
                    p_mui_list_view->selected_cb(
                        MUI_LIST_VIEW_EVENT_LONG_SELECTED, p_mui_list_view,
                        mui_list_item_array_get(p_mui_list_view->items, p_mui_list_view->focus_index));
                }
            }
            break;
        }
    }
}

static void mui_list_view_on_enter(mui_view_t *p_view) {
    mui_list_view_t *p_mui_list_view = p_view->user_data;
    p_mui_list_view->first_draw = 0;
}

static void mui_list_view_on_exit(mui_view_t *p_view) {}

mui_list_view_t *mui_list_view_create() {
    mui_list_view_t *p_mui_list_view = mui_mem_malloc(sizeof(mui_list_view_t));

    mui_view_t *p_view = mui_view_create();
    p_view->user_data = p_mui_list_view;
    p_view->draw_cb = mui_list_view_on_draw;
    p_view->input_cb = mui_list_view_on_input;
    p_view->enter_cb = mui_list_view_on_enter;
    p_view->exit_cb = mui_list_view_on_exit;

    p_mui_list_view->p_view = p_view;
    p_mui_list_view->focus_index = 0;
    p_mui_list_view->scroll_offset = 0;
    p_mui_list_view->selected_cb = NULL;
    p_mui_list_view->anim_value = 0;
    p_mui_list_view->anim_type = LIST_ANIM_FOCUS;

    mui_anim_init(&p_mui_list_view->anim);
    mui_anim_set_var(&p_mui_list_view->anim, p_mui_list_view);
    mui_anim_set_path_cb(&p_mui_list_view->gap_anim, lv_anim_path_ease_in_out);
    mui_anim_set_exec_cb(&p_mui_list_view->anim, mui_list_view_anim_exec);
    mui_anim_set_values(&p_mui_list_view->anim, 0, LIST_ITEM_HEIGHT);
    mui_anim_set_time(&p_mui_list_view->anim, 200);

    p_mui_list_view->text_offset = 0;

    mui_anim_init(&p_mui_list_view->text_anim);
    mui_anim_set_var(&p_mui_list_view->text_anim, p_mui_list_view);
    mui_anim_set_path_cb(&p_mui_list_view->text_anim, lv_anim_path_linear);
    mui_anim_set_exec_cb(&p_mui_list_view->text_anim, mui_list_view_text_anim_exec);
    mui_anim_set_time(&p_mui_list_view->text_anim, 200);

    mui_anim_init(&p_mui_list_view->gap_anim);
    mui_anim_set_var(&p_mui_list_view->gap_anim, p_mui_list_view);
    mui_anim_set_path_cb(&p_mui_list_view->gap_anim, lv_anim_path_ease_in_out);
    mui_anim_set_values(&p_mui_list_view->gap_anim, 0, LIST_ITEM_HEIGHT);
    mui_anim_set_exec_cb(&p_mui_list_view->gap_anim, mui_list_view_gap_anim_exec);
    mui_anim_set_time(&p_mui_list_view->gap_anim, 200);
    p_mui_list_view->item_gap = mui_list_view_anim_enabled() ? 0 : LIST_ITEM_HEIGHT;

    mui_list_item_array_init(p_mui_list_view->items);

    return p_mui_list_view;
}

void mui_list_view_free(mui_list_view_t *p_view) {
    mui_list_item_array_it_t it;

    mui_anim_stop(&p_view->anim);
    mui_anim_stop(&p_view->text_anim);

    mui_list_item_array_it(it, p_view->items);
    while (!mui_list_item_array_end_p(it)) {
        mui_list_item_t *item = mui_list_item_array_ref(it);
        string_clear(item->text);
        mui_list_item_array_next(it);
    }
    mui_list_item_array_clear(p_view->items);
    mui_mem_free(p_view->p_view);
    mui_mem_free(p_view);
}

mui_view_t *mui_list_view_get_view(mui_list_view_t *p_view) { return p_view->p_view; }

//// view functions //
void mui_list_view_add_item(mui_list_view_t *p_view, uint32_t icon, const char *text, void *user_data) {
    mui_list_view_add_item_ext(p_view, icon, text, NULL, user_data);
}

void mui_list_view_add_item_ext(mui_list_view_t *p_view, uint32_t icon, const char *text, const char *sub_text,
                                void *user_data) {
    mui_list_item_t *p_item = mui_list_item_array_push_new(p_view->items);
    p_item->icon = icon;
    p_item->user_data = user_data;
    string_init(p_item->text);
    string_init(p_item->sub_text);
    string_set_str(p_item->text, text);
    if (sub_text != NULL) {
        string_set_str(p_item->sub_text, sub_text);
    }
}

void mui_list_view_set_item(mui_list_view_t *p_view, uint16_t index, uint32_t icon, char *text, void *user_data) {
    mui_list_item_t *p_item = mui_list_item_array_get(p_view->items, index);
    if (p_item != NULL) {
        p_item->icon = icon;
        p_item->user_data = user_data;
        string_set_str(p_item->text, text);
    }
}

uint32_t mui_list_view_item_size(mui_list_view_t *p_view) { return mui_list_item_array_size(p_view->items); }

void mui_list_view_clear_items(mui_list_view_t *p_view) {
    mui_list_item_array_it_t it;

    mui_list_item_array_it(it, p_view->items);
    while (!mui_list_item_array_end_p(it)) {
        mui_list_item_t *item = mui_list_item_array_ref(it);
        string_clear(item->text);
        string_clear(item->sub_text);
        mui_list_item_array_next(it);
    }
    mui_list_item_array_reset(p_view->items);
    mui_list_view_set_focus(p_view, 0);
}

void mui_list_view_clear_items_with_cb(mui_list_view_t *p_view, mui_list_view_item_clear_cb clear_cb) {
    mui_list_item_array_it_t it;

    mui_list_item_array_it(it, p_view->items);
    while (!mui_list_item_array_end_p(it)) {
        mui_list_item_t *item = mui_list_item_array_ref(it);
        string_clear(item->text);
        string_clear(item->sub_text);
        clear_cb(item);
        mui_list_item_array_next(it);
    }
    mui_list_item_array_reset(p_view->items);
    mui_list_view_set_focus(p_view, 0);
}

void mui_list_view_set_selected_cb(mui_list_view_t *p_view, mui_list_view_selected_cb selected_cb) {
    p_view->selected_cb = selected_cb;
}

void mui_list_view_set_user_data(mui_list_view_t *p_view, void *user_data) { p_view->user_data = user_data; }

void mui_list_view_set_focus(mui_list_view_t *p_view, uint16_t focus_index) {
    if (focus_index >= 0 && focus_index < mui_list_item_array_size(p_view->items)) {
        p_view->focus_index = focus_index;
        uint32_t offset_y = p_view->focus_index * LIST_ITEM_HEIGHT;
        p_view->scroll_offset = offset_y;
    } else {
        p_view->focus_index = 0;
        p_view->scroll_offset = 0;
    }
}

uint16_t mui_list_view_get_focus(mui_list_view_t *p_view) { return p_view->focus_index; }

void mui_list_view_sort(mui_list_view_t *p_view, mui_list_view_item_cmp_cb cmp_cb) {
    mui_list_item_array_special_sort(p_view->items, cmp_cb);
}
