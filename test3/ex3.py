import os, json

# 获取脚本所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建json文件的完整路径
json_path = os.path.join(script_dir, "addressbook.json")

ab = {} #通信录保存在字典中name:tel
#从JSON文件中读取通信录
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        ab = json.load(f)

# 显示主菜单函数
def show_menu():
    print("\n===== 通讯录管理系统 =====")
    print("1. 显示通讯录清单")
    print("2. 查询联系人")
    print("3. 插入新的联系人")
    print("4. 删除已有联系人")
    print("5. 退出")
    print("========================")
    choice = input("请输入您的选择(1-5): ")
    return choice

# 显示通讯录清单
def show_all_contacts():
    if not ab:
        print("通讯录为空")
    else:
        print("\n===== 通讯录清单 =====")
        for name, tel in ab.items():
            print(f"姓名：{name}, 电话：{tel}")
        print("===================")

# 查询联系人
def search_contact():
    name = input("请输入要查询的联系人姓名: ")
    if name in ab:
        print(f"联系人: {name}, 电话: {ab[name]}")
    else:
        print(f"联系人 {name} 不存在")
        choice = input("是否新建该联系人? (y/n): ")
        if choice.lower() == 'y':
            add_contact(name)

# 新增联系人
def add_contact(name=None):
    if name is None:
        name = input("请输入新联系人姓名: ")
    
    if name in ab:
        print(f"联系人 {name} 已存在，电话: {ab[name]}")
        choice = input("是否更新该联系人信息? (y/n): ")
        if choice.lower() == 'y':
            tel = input("请输入新的电话号码: ")
            ab[name] = tel
            print(f"联系人 {name} 的电话已更新为 {tel}")
    else:
        tel = input("请输入电话号码: ")
        ab[name] = tel
        print(f"联系人 {name} 已添加到通讯录")

# 删除联系人
def delete_contact():
    name = input("请输入要删除的联系人姓名: ")
    if name in ab:
        del ab[name]
        print(f"联系人 {name} 已从通讯录中删除")
    else:
        print(f"联系人 {name} 不存在")

# 保存通讯录到文件
def save_addressbook():
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(ab, f, ensure_ascii=False)
    print("通讯录已保存")

# 主程序
def main():
    while True:
        choice = show_menu()
        
        if choice == '1':
            show_all_contacts()
        elif choice == '2':
            search_contact()
        elif choice == '3':
            add_contact()
        elif choice == '4':
            delete_contact()
        elif choice == '5':
            save_addressbook()
            print("感谢使用通讯录管理系统，再见！")
            break
        else:
            print("无效的选择，请重新输入")

if __name__ == "__main__":
    main()