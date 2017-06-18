from subprocess import check_output, list2cmdline

schema = 'org.gnome.settings-daemon.plugins.media-keys'
schema_slash = schema.replace(".", "/")
KB = "custom-keybinding"
KBS = "{}s".format(KB)


def list_all(verbose=False):
    if verbose:
        layout = "index: {}\nname: {}\ncommand: {}\nbinding: {}\n"
    else:
        layout = "{}, {}, {}, {}"
    print()
    for i in get_shortcut_indices():
        print(layout.format(i,
                            get_value(i, 'name')[1:-1],
                            get_value(i, 'command')[1:-1],
                            get_value(i, 'binding')[1:-1]))


def get_shortcut_indices():
    current = get_shortcuts()
    trim_str = '/{}/{}/custom'.format(schema_slash, KBS)
    tstr_len = len(trim_str)
    indices = []
    for c in current:
        assert c[:tstr_len] == trim_str
        indices.append(int(c[tstr_len:-1]))
    return indices


def get_value(index, field):
    args = [schema_path_for_index(index), field]
    return get(args)


def get_shortcuts():
    shortcuts = get([schema, KBS])
    if shortcuts == '@as []':
        return []
    return eval(shortcuts)


def path_for_index(index):
    return '/{}/{}/custom{}/'.format(schema_slash, KBS, index)


def schema_path_for_path(path):
    return '{}.{}:{}'.format(schema, KB, path)


def schema_path_for_index(index):
    return schema_path_for_path(path_for_index(index))


def run(args, verbose=False):
    if verbose:
        print("RUNNING: {}".format(list2cmdline(args)))
    return check_output(args).decode("utf-8").strip()


def get(args):
    fargs = ['gsettings', 'get'] + args
    return run(fargs)


def clear_shortcut(index=None, name=None, verbose=False):
    i = index if index else index_from_name(name)
    r = run(['gsettings', 'reset-recursively', schema_path_for_index(i)])
    remove_shortcut(i)
    return r


def index_from_name(name):
    values = []
    for i in get_shortcut_indices():
        value = get_value(i, 'name')[1:-1]  # strip first and last to remove quote marks
        if name == value:
            return i
        values.append(value)
    raise ValueError("existing names are {}".format(values))


def set_shortcut(name, command, binding, verbose=False):

    n = get_next_available_index()

    set_field(n, 'name', name)
    set_field(n, 'command', command)
    set_field(n, 'binding', binding)

    append_shortcut(n)
    return n


def get_next_available_index():
    n = 0
    indices = get_shortcut_indices()
    while True:
        if n in indices:
            n += 1
        else:
            break
    return n


def append_shortcut(index):
    shortcuts = get_shortcuts()
    shortcuts.append(path_for_index(index))
    set_shortcuts('{}'.format(shortcuts))


def remove_shortcut(index):
    shortcuts = get_shortcuts()
    shortcuts.remove(path_for_index(index))
    set_shortcuts('{}'.format(shortcuts))


def set_field(index, field, value):
    run(['gsettings', 'set', schema_path_for_index(index), field, to_val(value)])


def to_val(value):
    return "'{}'".format(value)


def set_shortcuts(newlist):
    run(['gsettings', 'set', schema, KBS, newlist])
