from androguard.core.apk import APK
from androguard.core.dex import DEX
import sys
from androguard.util import set_log
from elftools.elf.elffile import ELFFile
import io

set_log("ERROR")

def green(string):
    GREEN = '\033[92m'
    RESET = '\033[0m'
    return GREEN + string + RESET

def yellow(string):
  YELLOW = '\033[93m'
  RESET = '\033[0m'
  return YELLOW + string + RESET

def red(string):
  RED = '\033[91m'
  RESET = '\033[0m'
  return RED + string + RESET

def to_dalvik_format(class_name):
    return 'L' + class_name.replace('.', '/') + ';'

def get_entry_class_methods_and_fields(apk_object, entry_class_name):

    entry_class_name = to_dalvik_format(entry_class_name)
    methods = []
    fields = []

    for apk in apk_object.get_all_dex():
        d = DEX(apk)
        for cls in d.get_classes():
            if cls.get_name() == entry_class_name:
                for method in cls.get_methods():
                    methods.append(method.get_name())

                for field in cls.get_fields():
                    fields.append(field.get_name())

                return entry_class_name, methods, fields
    else:
        print(f"{entry_class_name} not found in DEX")
    return entry_class_name, methods, fields



def get_elf_info(elf_bytes):
    # 将 ELF 字节数据转换为文件对象
    elf_file_obj = io.BytesIO(elf_bytes)
    non_zero_size_funcs = []
    zero_size_funcs = []
    comments = []
    notes = []
    try:
        elf_file = ELFFile(elf_file_obj)
        # Iterate through sections to find symbol tables
        for section in elf_file.iter_sections():
            if section.name == '.dynsym' or section.name == '.symtab':
                # Iterate through symbols and extract function names
                for symbol in section.iter_symbols():
                    if symbol['st_info']['type'] == 'STT_FUNC':
                        if symbol['st_size'] != 0:
                            non_zero_size_funcs.append(symbol.name)
                        else:
                            zero_size_funcs.append(symbol.name)
            elif section.name.startswith('.comment'):
                comment = section.data().decode('utf-8').strip('\x00')
                comments.append(comment)
            elif section.name.startswith('.note'):
                for note in section.iter_notes():
                    notes.append(note)
        return non_zero_size_funcs, zero_size_funcs, comments, notes

    except Exception as e:
        print("Error: Unable to read ELF information - {}".format(str(e)))
        return non_zero_size_funcs, zero_size_funcs, comments, notes


apk_file = sys.argv[1]

# apk_file = "/Users/xxx/Downloads/wifi/xxx.apk"
# apk_file = "/Users/xxx/Downloads/xxx.apk"

apk = APK(apk_file)

print(red("====================== java info ==========================="))
print(yellow("FileName: "), apk_file.split("/")[-1])
# Get the name of the Application class from the AndroidManifest.xml
manifest = apk.get_android_manifest_xml()
application_element = manifest.find('application')
application_class_name = application_element.get('{http://schemas.android.com/apk/res/android}name')
if application_class_name.startswith('.'):
    application_class_name = apk.package_name + application_class_name
print(yellow("Applicatoin: "), application_class_name)

entry_class_name = apk.get_main_activity()
print(yellow("Entry Class: "), entry_class_name)

entry_class, methods, fields = get_entry_class_methods_and_fields(apk, entry_class_name)
print(yellow("Methods: "), methods)
print(yellow("Fields: "), fields)

# Get all files from the APK
files = apk.get_files()

print("")
print(red("======================= so info start ======================"))
for file in files:
    if file.endswith(".so"):
        elf_bytes = apk.get_file(file)
        non_zero_size_funcs, zero_size_funcs, comments, notes = get_elf_info(elf_bytes)
        print(f"{green(file)}\tSize: {str(len(elf_bytes)//1024)}KB\tFunction Count: {len(non_zero_size_funcs)}\tSyscall Count: {len(zero_size_funcs)}\tNote Count: {len(notes)}")
        # print("Functions: ", non_zero_size_funcs)
        print("Comments: ", ','.join(comments))
        print("-"*60)
print(red("======================= so info end ========================"))




