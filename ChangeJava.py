import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import sys
import subprocess

def rca(command):
    """以管理员身份运行指定的 CMD 命令"""
    try:
        # 使用 PowerShell 的 Start-Process 命令以管理员身份运行 CMD 命令
        subprocess.run(
            f"powershell Start-Process -FilePath 'cmd.exe' -ArgumentList '/c {command}' -Verb RunAs",
            shell=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"命令执行失败: {e.stderr}")

def get_base_path():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的程序，使用 .exe 文件所在目录
        base_path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        # 如果是直接运行脚本，使用脚本所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

def check_java():
    # 获取当前脚本所在的目录或打包后的 .exe 文件所在目录
    base_path = get_base_path()
    
    # 获取当前目录下的所有文件夹
    all_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    
    # 定义 Java 运行环境的特征文件
    java_marker_file = "bin/java.exe"
    
    java_folders = []
    
    # 遍历每个文件夹，检查是否存在 Java 运行环境的特征文件
    for folder in all_folders:
        folder_path = os.path.join(base_path, folder)
        marker_path = os.path.join(folder_path, java_marker_file)
        if os.path.exists(marker_path):
            java_folders.append(folder_path)
    
    return java_folders

def cjh(jh):
    if jh:
        # 替换路径中的反斜杠为双反斜杠
        rca(f"setx /M JAVA_HOME {jh}")
        messagebox.showinfo("更改完成", f"已更改Java环境为\n{jh}")
    else:
        messagebox.showwarning("未选择 Java", "未选择 Java，请选择 Java 环境")

def get_jh():
    selected_jh = dropdown.get()
    if selected_jh:
        cjh(selected_jh)
    else:
        messagebox.showwarning("未选择 Java", "未选择 Java，请选择 Java 环境")

# 设置工作目录为脚本所在目录或打包后的 .exe 文件所在目录
os.chdir(get_base_path())

# 创建主窗口
Window = tk.Tk()
style = ttk.Style()
style.theme_use("clam")
Window.title("Java环境切换")
Window.geometry("300x200")

# 添加标题
title = tk.Label(Window, text="请选择Java环境", font=("Arial", 16))
title.place(x=70, y=20)

# 检测 Java 环境
javas = check_java()

# 创建下拉菜单
dropdown = ttk.Combobox(Window, values=javas)
dropdown.place(x=68, y=50)

# 创建按钮
cje = ttk.Button(Window, text="更改Java环境", command=get_jh)
cje.place(x=180, y=150)

# 启动主循环
Window.mainloop()