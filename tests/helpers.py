import os


def find_test_resources_dir(start_dir):
    dirname, basename = os.path.split(start_dir)
    potential_dir = os.path.join(start_dir, 'test_resources')

    if os.path.isdir(potential_dir):
        return potential_dir
    else:
        if dirname == '/' and not basename:
            return None
        else:
            return find_test_resources_dir(dirname)
