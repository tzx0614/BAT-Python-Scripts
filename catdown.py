#! python3
# Categorizes files in "Downloads" into folders

import os
import shutil
import time

start_time = time.time()

HOME_DIR = os.path.expanduser("~")
DOWNLOADS_DIR = os.path.join(HOME_DIR, "Downloads")

folders_created: list = []
file_extensions: list = []
category_folder_paths: list = []
moved_files_count: dict = {}
file_replicate_count: dict = {}
moved_file_replicates_count: dict = {}


class File_Handling:
    @staticmethod
    def __get_file_extension(file):
        file_basename, file_extension = os.path.splitext(file)
        file_extension = file_extension[1:]
        return file_extension

    @staticmethod
    def determine_executables_present():
        for file_name in os.listdir(DOWNLOADS_DIR):
            file_path = os.path.join(DOWNLOADS_DIR, file_name)
            if os.path.isfile(file_path):
                file_extension = File_Handling.__get_file_extension(file_name)
                if file_extension not in file_extensions:
                    file_extensions.append(file_extension)

    @staticmethod
    def __create_folder(folder):
        folder_path = os.path.join(DOWNLOADS_DIR, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            folders_created.append(folder)
        return folder_path

    @staticmethod
    def create_categorical_folders():
        for file_extension in file_extensions:
            file_extension = file_extension.upper() + " Files"
            folder_path = File_Handling.__create_folder(file_extension)
            if folder_path is not None:
                category_folder_paths.append(folder_path)

    @staticmethod
    def __increment_dictionary_key_value(dictionary, key):
        dictionary.setdefault(key, 0)
        dictionary[key] += 1

    @staticmethod
    def __count_same_file_names(file, directory_path):
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            argument_file_extension = File_Handling.__get_file_extension(file)
            current_file_extension = File_Handling.__get_file_extension(file_name)
            are_files_same_extension = argument_file_extension == current_file_extension
            if os.path.isfile(file_path) and are_files_same_extension and len(file_name) >= len(file):
                start_index = 0
                if len(file_name) > len(file):
                    start_index = len(file_name) - len(file)
                file_name = file_name[start_index:]
                if file == file_name:
                    File_Handling.__increment_dictionary_key_value(file_replicate_count, file)

    @staticmethod
    def __rename_replicate_file(file):
        file_replicate_number = file_replicate_count[file]
        new_file_name = f"[{file_replicate_number}] - {file}"
        return new_file_name

    @staticmethod
    def __get_category_folder_path(file):
        file_extension = File_Handling.__get_file_extension(file)
        file_extension_index = file_extensions.index(file_extension)
        category_folder_path = category_folder_paths[file_extension_index]
        return category_folder_path

    @staticmethod
    def move_files_to_categorical_folders():
        for file_name in os.listdir(DOWNLOADS_DIR):
            file_path = os.path.join(DOWNLOADS_DIR, file_name)
            if os.path.isfile(file_path):
                file_extension = File_Handling.__get_file_extension(file_name)
                category_folder_path = File_Handling.__get_category_folder_path(file_name)
                file_destination_path = os.path.join(category_folder_path, file_name)
                if not os.path.exists(file_destination_path):
                    File_Handling.__increment_dictionary_key_value(moved_files_count, file_extension.upper())
                    shutil.move(src=file_path, dst=category_folder_path)
                else:
                    File_Handling.__count_same_file_names(file_name, category_folder_path)
                    new_file_name = File_Handling.__rename_replicate_file(file_name)
                    file_destination_path = os.path.join(category_folder_path, new_file_name)
                    File_Handling.__increment_dictionary_key_value(moved_file_replicates_count, file_name)
                    shutil.move(src=file_path, dst=file_destination_path)


class Show_Report:
    left_justify_main = 35
    right_justify_main = 10

    @staticmethod
    def __print_folder_creation_report(left_justify=left_justify_main, right_justify=right_justify_main):
        center_justify = left_justify + right_justify
        folder_created_statement = None
        if len(folders_created) != 0:
            if len(folders_created) == 1:
                folder_created_statement = f"  FOLDER CREATED: {len(folders_created)}  "
            elif len(folders_created) > 1:
                folder_created_statement = f"  FOLDERS CREATED: {len(folders_created)}  "
            print(folder_created_statement.center(center_justify, "-"))
            for count, folder_created in enumerate(sorted(folders_created), 1):
                print(f"  {count}. {folder_created}")
        else:
            folder_created_statement = "  NO FOLDERS CREATED  "
            print(folder_created_statement.center(center_justify, "-"))

    @staticmethod
    def startup_description(left_justify=left_justify_main, right_justify=right_justify_main):
        center_justify = left_justify + right_justify
        print("\'Downloads\' Folder Organizer v.3.5".center(center_justify))
        print()
        Show_Report.__print_folder_creation_report()
        print()

    @staticmethod
    def __sum_value(dictionary):
        value_total = 0
        for value in dictionary.values():
            value_total += value
        return value_total

    @staticmethod
    def __print_table(dictionary, left_justify=left_justify_main, right_justify=right_justify_main):
        for key in sorted(dictionary.keys()):
            value = dictionary[key]
            display_key = f"  {key}  ".ljust(left_justify, ".")
            display_value = f"  {value}  ".rjust(right_justify, ".")
            print(f"{display_key}{display_value}")
            print()

    @staticmethod
    def __print_organization_report(left_justify=left_justify_main, right_justify=right_justify_main):
        center_justify = left_justify + right_justify
        if moved_files_count:
            print("Organizing \'Downloads\' Folder Finished!".center(center_justify))
            print()
            print()
            print("  ORGANIZATION REPORT  ".center(center_justify, "-"))
            Show_Report.__print_table(moved_files_count)

    @staticmethod
    def __print_total_files_moved(total_files_moved, left_justify=left_justify_main, right_justify=right_justify_main):
        center_justify = left_justify + right_justify
        ending_statement = None
        if moved_files_count:
            if total_files_moved > 1:
                ending_statement = f"HAVING A TOTAL OF {total_files_moved} FILES MOVED!"
            elif total_files_moved == 1:
                ending_statement = f"HAVING A TOTAL OF {total_files_moved} FILE MOVED!"
        else:
            if file_replicate_count:
                ending_statement = "THE \'DOWNLOADS\' FOLDER CONTAINS REPLICATES!"
            else:
                ending_statement = "THE \'DOWNLOADS\' FOLDER IS ALREADY CLEAN!"
        print(ending_statement.center(center_justify))
        print()

    @staticmethod
    def __print_replicate_report(total_replicate_files, left_justify=left_justify_main,
                                 right_justify=right_justify_main):
        center_justify = left_justify + right_justify
        replicate_statement = None
        if total_replicate_files != 0:
            if total_replicate_files == 1:
                replicate_statement = f"  THERE ARE {total_replicate_files} REPLICATE DISCOVERED  "
            elif total_replicate_files > 1:
                replicate_statement = f"  THERE ARE {total_replicate_files} REPLICATES DISCOVERED  "
            print(replicate_statement.center(center_justify, "-"))
            print()
            Show_Report.__print_table(moved_file_replicates_count)
        else:
            replicate_statement = "  THERE ARE NO REPLICATES DISCOVERED  "
            print(replicate_statement.center(center_justify, "-"))
            print()

    @staticmethod
    def __print_total_time(left_justify=left_justify_main, right_justify=right_justify_main):
        center_justify = left_justify + right_justify
        end_time = time.time()
        total_time = round(end_time - start_time, 3)
        time_statement = None
        if moved_files_count:
            if total_time <= 1:
                time_statement = f"IT TOOK {total_time} SECOND TO ORGANIZE"
            elif total_time > 1:
                time_statement = f"IT TOOK {total_time} SECONDS TO ORGANIZE"
        else:
            if total_time <= 1:
                time_statement = f"IT TOOK {total_time} SECOND TO CHECK"
            elif total_time > 1:
                time_statement = f"IT TOOK {total_time} SECONDS TO CHECK"
        print(time_statement.center(center_justify))

    @staticmethod
    def print_report():
        total_files_moved = Show_Report.__sum_value(moved_files_count)
        total_replicate_files = Show_Report.__sum_value(file_replicate_count)
        Show_Report.__print_organization_report()
        Show_Report.__print_total_files_moved(total_files_moved)
        Show_Report.__print_replicate_report(total_replicate_files)
        Show_Report.__print_total_time()

    @staticmethod
    def prevent_immediate_close(left_justify=left_justify_main, right_justify=right_justify_main):
        center_justify = left_justify + right_justify
        print()
        input("Press Any Key To Close.".center(center_justify))


if __name__ == "__main__":
    File_Handling.determine_executables_present()
    File_Handling.create_categorical_folders()
    Show_Report.startup_description()
    File_Handling.move_files_to_categorical_folders()
    Show_Report.print_report()
    Show_Report.prevent_immediate_close()
