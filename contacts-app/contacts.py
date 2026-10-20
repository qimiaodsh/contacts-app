# 联系人管理系统（CLI + SQLite）
# 运行：python contacts.py

import sqlite3
import csv

conn = sqlite3.connect("contacts.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    name TEXT PRIMARY KEY,
    phone TEXT
)
""")
conn.commit()


def add_contact(name, phone):
    name = name.strip()
    phone = phone.strip()

    if not name:
        print("姓名不能为空")
        return
    if not phone.isdigit():
        print("电话只能是数字")
        return

    conn.execute("INSERT OR REPLACE INTO contacts VALUES (?, ?)", (name, phone))
    conn.commit()
    print(f"已保存 {name}")


def get_contact(name):
    row = conn.execute(
        "SELECT phone FROM contacts WHERE name = ?", (name,)
    ).fetchone()
    if row is None:
        return None
    return row[0]


def list_contacts():
    return conn.execute("SELECT name, phone FROM contacts").fetchall()


def delete_contact(name):
    conn.execute("DELETE FROM contacts WHERE name = ?", (name,))
    conn.commit()


def search_contacts(keyword):
    return conn.execute(
        "SELECT name, phone FROM contacts WHERE name LIKE ?",
        (f"%{keyword}%",),
    ).fetchall()


def export_csv():
    rows = list_contacts()
    with open("contacts_export.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["姓名", "电话"])
        writer.writerows(rows)
    print("已导出 contacts_export.csv")


def main():
    while True:
        print("\n===== 通讯录（SQLite）=====")
        print("1. 添加/修改联系人")
        print("2. 查询联系人")
        print("3. 查看全部")
        print("4. 删除联系人")
        print("5. 搜索联系人")
        print("6. 导出 CSV")
        print("0. 退出")
        choice = input("请选择：")

        if choice == "1":
            name = input("姓名：")
            phone = input("电话：")
            add_contact(name, phone)

        elif choice == "2":
            name = input("姓名：")
            phone = get_contact(name)
            print(phone if phone else "没找到")

        elif choice == "3":
            rows = list_contacts()
            if not rows:
                print("还没有联系人")
            else:
                for name, phone in rows:
                    print(name, phone)

        elif choice == "4":
            name = input("姓名：")
            delete_contact(name)
            print("已删除")

        elif choice == "5":
            keyword = input("搜索关键词：")
            rows = search_contacts(keyword)
            if not rows:
                print("没有匹配的联系人")
            else:
                for name, phone in rows:
                    print(name, phone)

        elif choice == "6":
            export_csv()

        elif choice == "0":
            conn.close()
            print("再见")
            break

        else:
            print("没有这个选项，请重新选择")


if __name__ == "__main__":
    main()
