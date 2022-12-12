import difflib
def bug_catcher(func):

    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ValueError as exc:
            return exc.args[0]
        except KeyError as exc:
            return f"Wrong information: {exc.args[0]}"
        except Warning as exc:
            return find_word_with_wrong_key(exc.args[0])
        except IndexError:
            return f"Not enough information for this command."
        except TypeError as exc:
            return exc.args[0]
        except FileExistsError as exc:
            return exc.args[0]
        except FileNotFoundError as exc:
            return exc.args[0]

    return inner

def find_word_with_wrong_key(srch: str) -> str:
    search_words = srch.split("_")
    result_list,result_dict  = [], {}
    com = ['help', 'instruction', 'create', 'add_phone', 'add_email', 'add_address', 'set_birthday', 'show_birthdays', 'days_to',
           'birthday_for_all', 'edit_contact', 'edit_name', 'search', 'search_info', 'show', 'clear_book', 'create_note', 'add_note',
           'clear_note', 'clear_tags', 'clear_text', 'delete_note', 'search_in_text', 'search_in_tags', 'sorted_by_tags', 'show_note',
           'show_note_book', 'file_sorter', 'exit']
    for words in com:
        cnt = 0
        for word_from_commands in words.split("_"):
            for word_from_search in search_words:
                cnt += 1 if word_from_search == word_from_commands else 0
        mathcer = difflib.SequenceMatcher(None, srch, words)
        # print(f"{words} --- {mathcer.ratio()}")
        if mathcer.ratio() >= 0.5:
            result_dict[words] = f"{round(mathcer.ratio(), 2)*100}%"
        if cnt >= 1:
            result_list.append([cnt, words])

    return f"\nI can't find command '{srch}'.\n" \
           f"Did you mean:\n" \
           f"{[v[1] for v in sorted(result_list, reverse=True)] if result_list else '<<<I cant find something similar.>>>'}\n" \
           f"Or you can find your command here:\n" \
           f"{[f'{k}: {value}' for k, value in result_dict.items()] if result_dict else '<<<I cant find something similar.>>>'}"

# def bug_catcher(func):
#     def inner(*args, ** kwargs):
#         return func(args, kwargs)
#     return inner