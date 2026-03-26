# -*- coding: utf-8 -*-
"""
项目文件管理系统 V1.0
作者：小不点
功能：项目导向的文件管理，支持时间线、标签、搜索
"""

import os
import shutil
import json
import sqlite3
from datetime import datetime
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading

# ==================== 配置 ====================
BASE_DIR = r"D:\项目管理"  # 项目存储根目录
DB_FILE = os.path.join(BASE_DIR, "projects.db")  # 数据库文件

# 默认项目阶段
DEFAULT_STAGES = ["01_资料收集", "02_进行中", "03_深化扩展", "04_归档"]

# ==================== 数据库初始化 ====================
def init_db():
    """初始化数据库"""
    os.makedirs(BASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 项目表 - 添加父项目字段支持子项目
    c.execute('''CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        created_at TEXT,
        updated_at TEXT,
        tags TEXT,
        status TEXT DEFAULT '进行中',
        parent_id INTEGER DEFAULT NULL,
        FOREIGN KEY (parent_id) REFERENCES projects(id)
    )''')
    
    # 时间线阶段表
    c.execute('''CREATE TABLE IF NOT EXISTS stages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        stage_name TEXT,
        stage_order INTEGER,
        created_at TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )''')
    
    # 文件记录表
    c.execute('''CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        stage_id INTEGER,
        filename TEXT,
        filepath TEXT,
        file_size INTEGER,
        file_type TEXT,
        tags TEXT,
        added_at TEXT,
        note TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (stage_id) REFERENCES stages(id)
    )''')
    
    conn.commit()
    conn.close()

# ==================== 核心功能类 ====================
class ProjectManager:
    """项目管理器"""
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()
    
    def create_project(self, name, description="", tags="", parent_id=None):
        """创建新项目，支持子项目"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 创建项目记录
        self.cur.execute(
            "INSERT INTO projects (name, description, tags, created_at, updated_at, parent_id) VALUES (?, ?, ?, ?, ?, ?)",
            (name, description, tags, now, now, parent_id)
        )
        project_id = self.cur.lastrowid
        
        # 确定项目路径
        if parent_id:
            # 子项目放在父项目文件夹下
            self.cur.execute("SELECT name FROM projects WHERE id = ?", (parent_id,))
            parent_name = self.cur.fetchone()[0]
            project_dir = os.path.join(BASE_DIR, parent_name, name)
        else:
            # 顶级项目
            project_dir = os.path.join(BASE_DIR, name)
        
        os.makedirs(project_dir, exist_ok=True)
        
        # 创建默认阶段文件夹
        for i, stage in enumerate(DEFAULT_STAGES):
            stage_dir = os.path.join(project_dir, stage)
            os.makedirs(stage_dir, exist_ok=True)
            
            # 记录到数据库
            self.cur.execute(
                "INSERT INTO stages (project_id, stage_name, stage_order, created_at) VALUES (?, ?, ?, ?)",
                (project_id, stage, i+1, now)
            )
        
        self.conn.commit()
        return project_id
    
    def get_all_projects(self, parent_id=None):
        """获取所有项目，支持按父项目过滤"""
        if parent_id is None:
            # 获取顶级项目
            self.cur.execute("SELECT id, name, description, tags, status, updated_at, parent_id FROM projects WHERE parent_id IS NULL ORDER BY updated_at DESC")
        else:
            # 获取子项目
            self.cur.execute("SELECT id, name, description, tags, status, updated_at, parent_id FROM projects WHERE parent_id = ? ORDER BY updated_at DESC", (parent_id,))
        return self.cur.fetchall()
    
    def get_project_tree(self):
        """获取项目树形结构"""
        # 获取所有顶级项目
        self.cur.execute("SELECT id, name, description, tags, status, updated_at FROM projects WHERE parent_id IS NULL ORDER BY name")
        top_projects = self.cur.fetchall()
        
        result = []
        for proj in top_projects:
            proj_id = proj[0]
            # 检查是否有子项目
            self.cur.execute("SELECT COUNT(*) FROM projects WHERE parent_id = ?", (proj_id,))
            child_count = self.cur.fetchone()[0]
            
            result.append({
                'id': proj_id,
                'name': proj[1],
                'description': proj[2],
                'tags': proj[3],
                'status': proj[4],
                'updated_at': proj[5],
                'has_children': child_count > 0,
                'child_count': child_count
            })
        
        return result
    
    def get_project_stages(self, project_id):
        """获取项目的时间线阶段"""
        self.cur.execute(
            "SELECT id, stage_name FROM stages WHERE project_id = ? ORDER BY stage_order",
            (project_id,)
        )
        return self.cur.fetchall()
    
    def get_stage_files(self, stage_id):
        """获取阶段下的所有文件"""
        self.cur.execute(
            "SELECT id, filename, filepath, file_size, tags, added_at, note FROM files WHERE stage_id = ? ORDER BY added_at DESC",
            (stage_id,)
        )
        return self.cur.fetchall()
    
    def add_file_to_stage(self, project_id, stage_id, source_path, tags="", note=""):
        """添加文件到指定阶段（归档模式：复制文件）"""
        filename = os.path.basename(source_path)
        file_size = os.path.getsize(source_path)
        file_type = os.path.splitext(filename)[1]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取阶段名称和项目名称
        self.cur.execute("SELECT stage_name FROM stages WHERE id = ?", (stage_id,))
        stage_name = self.cur.fetchone()[0]
        
        self.cur.execute("SELECT name FROM projects WHERE id = ?", (project_id,))
        project_name = self.cur.fetchone()[0]
        
        # 目标路径
        target_dir = os.path.join(BASE_DIR, project_name, stage_name)
        os.makedirs(target_dir, exist_ok=True)
        
        # 处理文件名冲突
        target_path = os.path.join(target_dir, filename)
        if os.path.exists(target_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(target_path):
                target_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
                counter += 1
            filename = os.path.basename(target_path)
        
        # 复制文件
        shutil.copy2(source_path, target_path)
        
        # 记录到数据库
        self.cur.execute(
            "INSERT INTO files (project_id, stage_id, filename, filepath, file_size, file_type, tags, added_at, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (project_id, stage_id, filename, target_path, file_size, file_type, tags, now, note)
        )
        
        # 更新项目更新时间
        self.cur.execute("UPDATE projects SET updated_at = ? WHERE id = ?", (now, project_id))
        
        self.conn.commit()
        return filename
    
    def search_files(self, keyword):
        """搜索文件"""
        keyword = f"%{keyword}%"
        self.cur.execute(
            "SELECT f.filename, f.tags, f.added_at, p.name, s.stage_name FROM files f "
            "JOIN projects p ON f.project_id = p.id "
            "JOIN stages s ON f.stage_id = s.id "
            "WHERE f.filename LIKE ? OR f.tags LIKE ? OR f.note LIKE ? OR p.name LIKE ? "
            "ORDER BY f.added_at DESC",
            (keyword, keyword, keyword, keyword)
        )
        return self.cur.fetchall()
    
    def get_project_stats(self, project_id):
        """获取项目统计"""
        # 文件数量
        self.cur.execute("SELECT COUNT(*) FROM files WHERE project_id = ?", (project_id,))
        file_count = self.cur.fetchone()[0]
        
        # 总大小
        self.cur.execute("SELECT SUM(file_size) FROM files WHERE project_id = ?", (project_id,))
        total_size = self.cur.fetchone()[0] or 0
        
        # 各阶段文件数
        self.cur.execute(
            "SELECT s.stage_name, COUNT(f.id) FROM stages s "
            "LEFT JOIN files f ON s.id = f.stage_id "
            "WHERE s.project_id = ? "
            "GROUP BY s.id",
            (project_id,)
        )
        stage_counts = self.cur.fetchall()
        
        return {
            "file_count": file_count,
            "total_size": total_size,
            "stage_counts": stage_counts
        }
    
    def delete_project(self, project_id):
        """删除项目"""
        # 获取项目名
        self.cur.execute("SELECT name FROM projects WHERE id = ?", (project_id,))
        result = self.cur.fetchone()
        if not result:
            return False
        
        project_name = result[0]
        
        # 删除数据库记录
        self.cur.execute("DELETE FROM files WHERE project_id = ?", (project_id,))
        self.cur.execute("DELETE FROM stages WHERE project_id = ?", (project_id,))
        self.cur.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        
        # 删除文件夹
        project_dir = os.path.join(BASE_DIR, project_name)
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        
        self.conn.commit()
        return True
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

# ==================== GUI界面 ====================
class ProjectFileManagerGUI:
    """项目文件管理器GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📁 项目文件管理系统 V1.0")
        self.root.geometry("1200x700")
        
        # 初始化数据库
        init_db()
        self.pm = ProjectManager()
        self.cur = self.pm.cur  # 引用数据库游标
        
        # 当前选中
        self.current_project_id = None
        self.current_stage_id = None
        
        # 颜色主题
        self.colors = {
            "bg": "#f5f5f5",
            "sidebar": "#2c3e50",
            "sidebar_text": "#ecf0f1",
            "accent": "#3498db",
            "success": "#27ae60",
            "warning": "#f39c12"
        }
        
        self.setup_ui()
        self.load_projects()
    
    def setup_ui(self):
        """设置UI"""
        # 主容器
        main_frame = Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill=BOTH, expand=True)
        
        # 顶部标题栏
        header = Frame(main_frame, bg=self.colors["sidebar"], height=60)
        header.pack(fill=X)
        header.pack_propagate(False)
        
        Label(header, text="📁 项目文件管理系统", font=("微软雅黑", 18, "bold"), 
              bg=self.colors["sidebar"], fg=self.colors["sidebar_text"]).pack(side=LEFT, padx=20)
        
        # 搜索框
        self.search_var = StringVar()
        self.search_var.trace("w", lambda *args: self.do_search())
        search_entry = Entry(header, textvariable=self.search_var, font=("微软雅黑", 11), width=25)
        search_entry.pack(side=RIGHT, padx=20, pady=12)
        Label(header, text="🔍 搜索：", bg=self.colors["sidebar"], fg=self.colors["sidebar_text"]).pack(side=RIGHT)
        
        # 左侧边栏 - 项目列表
        sidebar = Frame(main_frame, bg=self.colors["sidebar"], width=250)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)
        
        # 当前父项目ID（用于显示子项目）
        self.current_parent_id = None
        self.parent_stack = []  # 用于返回上级
        
        # 返回上级按钮
        self.btn_back = Button(sidebar, text="← 返回上级", font=("微软雅黑", 11), 
                               bg="#34495e", fg="white", relief=FLAT,
                               command=self.go_back_parent)
        self.btn_back.pack(fill=X, padx=10, pady=(10,5))
        self.btn_back.pack_forget()  # 初始隐藏
        
        # 按钮区域
        btn_frame_sidebar = Frame(sidebar, bg=self.colors["sidebar"])
        btn_frame_sidebar.pack(fill=X, padx=10, pady=10)
        
        # 新建项目按钮
        btn_new = Button(btn_frame_sidebar, text="+ 新建项目", font=("微软雅黑", 11), 
                         bg=self.colors["success"], fg="white", relief=FLAT,
                         command=lambda: self.create_project_dialog(self.current_parent_id))
        btn_new.pack(fill=X, pady=(0,5))
        
        # 创建子项目按钮（初始隐藏，选中项目后显示）
        self.btn_new_child = Button(btn_frame_sidebar, text="📁 创建子项目", font=("微软雅黑", 11), 
                                    bg=self.colors["accent"], fg="white", relief=FLAT,
                                    command=self.create_child_project)
        self.btn_new_child.pack(fill=X)
        self.btn_new_child.pack_forget()  # 初始隐藏
        
        # 项目列表标题
        self.lbl_project_title = Label(sidebar, text="📁 项目列表", font=("微软雅黑", 11, "bold"), 
              bg=self.colors["sidebar"], fg=self.colors["sidebar_text"])
        self.lbl_project_title.pack(anchor=W, padx=15, pady=(10,5))
        
        # 项目列表（使用Treeview支持层级）
        self.project_tree = ttk.Treeview(sidebar, show="tree", selectmode="browse")
        self.project_tree.pack(fill=BOTH, expand=True, padx=10, pady=5)
        self.project_tree.bind("<<TreeviewSelect>>", self.on_project_select)
        self.project_tree.bind("<Double-1>", self.on_project_double_click)
        
        # 中间内容区
        content = Frame(main_frame, bg=self.colors["bg"])
        content.pack(side=LEFT, fill=BOTH, expand=True)
        
        # 项目信息栏
        info_frame = Frame(content, bg="white", padx=15, pady=10)
        info_frame.pack(fill=X)
        
        self.lbl_project_name = Label(info_frame, text="选择或创建项目", font=("微软雅黑", 16, "bold"), bg="white")
        self.lbl_project_name.pack(side=LEFT)
        
        self.lbl_project_info = Label(info_frame, text="", font=("微软雅黑", 10), bg="white", fg="#7f8c8d")
        self.lbl_project_info.pack(side=LEFT, padx=15)
        
        # 时间线/阶段栏
        self.stage_frame = Frame(content, bg=self.colors["bg"])
        self.stage_frame.pack(fill=X, padx=15, pady=10)
        
        # 文件列表区域
        file_frame = Frame(content, bg="white")
        file_frame.pack(fill=BOTH, expand=True, padx=15, pady=(0,15))
        
        # 文件表格
        columns = ("filename", "tags", "size", "date", "note")
        self.file_tree = ttk.Treeview(file_frame, columns=columns, show="headings", selectmode="browse")
        
        self.file_tree.heading("filename", text="文件名")
        self.file_tree.heading("tags", text="标签")
        self.file_tree.heading("size", text="大小")
        self.file_tree.heading("date", text="添加日期")
        self.file_tree.heading("note", text="备注")
        
        self.file_tree.column("filename", width=300)
        self.file_tree.column("tags", width=150)
        self.file_tree.column("size", width=80)
        self.file_tree.column("date", width=120)
        self.file_tree.column("note", width=200)
        
        self.file_tree.pack(fill=BOTH, expand=True)
        
        # 右键菜单
        self.file_menu = Menu(self.file_tree, tearoff=0)
        self.file_menu.add_command(label="打开文件", command=self.open_file)
        self.file_menu.add_command(label="打开所在文件夹", command=self.open_folder)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="删除记录", command=self.delete_file_record)
        self.file_tree.bind("<Button-3>", self.show_file_menu)
        
        # 底部状态栏
        status_frame = Frame(content, bg="#ecf0f1", padx=15, pady=5)
        status_frame.pack(fill=X, side=BOTTOM)
        
        self.lbl_status = Label(status_frame, text="就绪", bg="#ecf0f1", fg="#7f8c8d")
        self.lbl_status.pack(side=LEFT)
        
        # 操作按钮栏（独立一行，更明显）
        action_frame = Frame(content, bg="#dfe6e9", padx=15, pady=8)
        action_frame.pack(fill=X)
        
        Label(action_frame, text="操作：", font=("微软雅黑", 10), bg="#dfe6e9").pack(side=LEFT)
        
        Button(action_frame, text="📄 添加文件", font=("微软雅黑", 10), width=12,
               bg=self.colors["accent"], fg="white", relief=RAISED, bd=2,
               command=self.add_files).pack(side=LEFT, padx=5)
        
        Button(action_frame, text="📂 添加文件夹", font=("微软雅黑", 10), width=12,
               bg="#8e44ad", fg="white", relief=RAISED, bd=2,
               command=self.add_folder).pack(side=LEFT, padx=5)
        
        Button(action_frame, text="🤖 智能归档", font=("微软雅黑", 10), width=12,
               bg=self.colors["warning"], fg="white", relief=RAISED, bd=2,
               command=self.smart_archive).pack(side=LEFT, padx=5)
    
    def load_projects(self):
        """加载项目列表 - 支持层级显示"""
        # 清空树
        for item in self.project_tree.get_children():
            self.project_tree.delete(item)
        
        if self.current_parent_id is None:
            # 显示顶级项目
            self.lbl_project_title.config(text="📁 项目列表")
            self.btn_back.pack_forget()
            projects = self.pm.get_project_tree()
            
            for p in projects:
                icon = "📁" if p['has_children'] else "📄"
                display = f"{icon} {p['name']}"
                if p['child_count'] > 0:
                    display += f" ({p['child_count']}个子项目)"
                
                self.project_tree.insert("", END, text=display, values=(p['id'],))
        else:
            # 显示子项目
            self.cur.execute("SELECT name FROM projects WHERE id = ?", (self.current_parent_id,))
            parent_name = self.cur.fetchone()[0]
            self.lbl_project_title.config(text=f"📂 {parent_name}")
            self.btn_back.pack(fill=X, padx=10, pady=(10,5))
            
            projects = self.pm.get_all_projects(self.current_parent_id)
            for p in projects:
                name = p[1]
                display = f"📄 {name}"
                self.project_tree.insert("", END, text=display, values=(p[0],))
    
    def go_back_parent(self):
        """返回上级项目"""
        if self.parent_stack:
            self.current_parent_id = self.parent_stack.pop()
        else:
            self.current_parent_id = None
        self.load_projects()
    
    def on_project_double_click(self, event):
        """双击项目 - 进入子项目或查看详情"""
        selection = self.project_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        project_id = self.project_tree.item(item, "values")[0]
        
        # 检查是否有子项目
        self.cur.execute("SELECT COUNT(*) FROM projects WHERE parent_id = ?", (project_id,))
        child_count = self.cur.fetchone()[0]
        
        if child_count > 0:
            # 进入子项目列表
            self.parent_stack.append(self.current_parent_id)
            self.current_parent_id = project_id
            self.load_projects()
        else:
            # 没有子项目，显示详情
            self.on_project_select(event)
    
    def on_project_select(self, event):
        """项目选中事件"""
        selection = self.project_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        project_id = self.project_tree.item(item, "values")[0]
        self.current_project_id = project_id
        
        # 显示创建子项目按钮
        self.btn_new_child.pack(fill=X, pady=(5,0))
        
        self.load_project_detail()
    
    def create_child_project(self):
        """为当前选中的项目创建子项目"""
        if not self.current_project_id:
            messagebox.showwarning("提示", "请先选择一个项目")
            return
        
        self.create_project_dialog(self.current_project_id)
    
    def load_project_detail(self):
        """加载项目详情"""
        if not self.current_project_id:
            return
        
        # 获取项目信息
        self.cur.execute("SELECT name, description, tags, updated_at FROM projects WHERE id = ?", 
                        (self.current_project_id,))
        proj = self.cur.fetchone()
        
        if proj:
            self.lbl_project_name.config(text=proj[0])
            self.lbl_project_info.config(text=f"标签: {proj[2] or '无'}  |  更新: {proj[3][:10]}")
        
        # 加载时间线阶段
        for widget in self.stage_frame.winfo_children():
            widget.destroy()
        
        stages = self.pm.get_project_stages(self.current_project_id)
        
        Label(self.stage_frame, text="🕐 时间线：", font=("微软雅黑", 11, "bold"), 
              bg=self.colors["bg"]).pack(side=LEFT, padx=(0,10))
        
        for stage_id, stage_name in stages:
            btn = Button(self.stage_frame, text=stage_name.replace("01_", "").replace("02_", "").replace("03_", "").replace("04_", ""),
                        font=("微软雅黑", 10), bg="white", relief=RAISED,
                        command=lambda sid=stage_id: self.select_stage(sid))
            btn.pack(side=LEFT, padx=5)
        
        # 默认显示第一个阶段
        if stages:
            self.select_stage(stages[0][0])
        
        # 更新统计
        self.update_stats()
    
    def select_stage(self, stage_id):
        """选择阶段"""
        self.current_stage_id = stage_id
        self.load_files()
    
    def load_files(self):
        """加载文件列表"""
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        if not self.current_stage_id:
            return
        
        files = self.pm.get_stage_files(self.current_stage_id)
        
        for f in files:
            file_id, filename, filepath, size, tags, date, note = f
            size_str = self.format_size(size)
            date_str = date[:10] if date else ""
            
            self.file_tree.insert("", END, values=(filename, tags or "", size_str, date_str, note or ""),
                                 tags=(str(file_id), filepath))
    
    def create_project_dialog(self, parent_id=None):
        """创建项目对话框，支持创建子项目"""
        dialog = Toplevel(self.root)
        
        if parent_id:
            # 获取父项目名
            self.cur.execute("SELECT name FROM projects WHERE id = ?", (parent_id,))
            parent_name = self.cur.fetchone()[0]
            dialog.title(f"新建子项目 - {parent_name}")
        else:
            dialog.title("新建项目")
        
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 确保对话框在最前面
        dialog.lift()
        dialog.focus_force()
        
        Frame(dialog, height=20).pack()
        
        # 显示父项目信息
        if parent_id:
            Label(dialog, text=f"父项目：{parent_name}", font=("微软雅黑", 10), fg="gray").pack(anchor=W, padx=20)
        
        Label(dialog, text="项目名称：", font=("微软雅黑", 11)).pack(anchor=W, padx=20, pady=(10,0))
        name_entry = Entry(dialog, font=("微软雅黑", 11), width=35)
        name_entry.pack(padx=20, pady=5)
        
        Label(dialog, text="项目描述：", font=("微软雅黑", 11)).pack(anchor=W, padx=20, pady=(10,0))
        desc_entry = Entry(dialog, font=("微软雅黑", 11), width=35)
        desc_entry.pack(padx=20, pady=5)
        
        Label(dialog, text="标签（逗号分隔）：", font=("微软雅黑", 11)).pack(anchor=W, padx=20, pady=(10,0))
        tags_entry = Entry(dialog, font=("微软雅黑", 11), width=35)
        tags_entry.pack(padx=20, pady=5)
        
        # 按钮区域
        btn_frame = Frame(dialog)
        btn_frame.pack(pady=20)
        
        def confirm():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("提示", "请输入项目名称", parent=dialog)
                return
            
            try:
                self.pm.create_project(name, desc_entry.get().strip(), tags_entry.get().strip(), parent_id)
                dialog.destroy()
                self.load_projects()
                
                if parent_id:
                    messagebox.showinfo("成功", f"子项目 '{name}' 创建成功！")
                else:
                    messagebox.showinfo("成功", f"项目 '{name}' 创建成功！")
            except Exception as e:
                messagebox.showerror("错误", f"创建失败：{str(e)}", parent=dialog)
        
        def cancel():
            dialog.destroy()
        
        Button(btn_frame, text="取消", font=("微软雅黑", 11), width=10,
               command=cancel).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="创建", font=("微软雅黑", 11), bg=self.colors["success"], fg="white", width=10,
               command=confirm).pack(side=LEFT, padx=10)
    
    def add_files(self):
        """添加单个或多个文件"""
        if not self.current_project_id or not self.current_stage_id:
            messagebox.showwarning("提示", "请先选择一个项目和阶段")
            return
        
        files = filedialog.askopenfilenames(title="选择文件（可多选）")
        if not files:
            return
        
        added = 0
        for f in files:
            try:
                self.pm.add_file_to_stage(self.current_project_id, self.current_stage_id, f)
                added += 1
            except Exception as e:
                print(f"添加失败: {f}, {e}")
        
        self.load_files()
        self.update_stats()
        messagebox.showinfo("完成", f"成功添加 {added} 个文件")
        self.lbl_status.config(text=f"已添加 {added} 个文件")
    
    def add_folder(self):
        """添加整个文件夹（递归归档所有文件）"""
        if not self.current_project_id or not self.current_stage_id:
            messagebox.showwarning("提示", "请先选择一个项目和阶段")
            return
        
        folder = filedialog.askdirectory(title="选择要归档的文件夹")
        if not folder:
            return
        
        # 扫描文件夹内所有文件
        all_files = []
        for root_dir, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                all_files.append(os.path.join(root_dir, file))
        
        if not all_files:
            messagebox.showinfo("提示", "文件夹为空")
            return
        
        if not messagebox.askyesno("确认", f"将归档「{os.path.basename(folder)}」文件夹中的 {len(all_files)} 个文件，确认吗？"):
            return
        
        added = 0
        for f in all_files:
            try:
                self.pm.add_file_to_stage(self.current_project_id, self.current_stage_id, f)
                added += 1
            except:
                pass
        
        self.load_files()
        self.update_stats()
        messagebox.showinfo("完成", f"成功归档 {added} 个文件")
    
    def open_file(self):
        """打开文件"""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = self.file_tree.item(selection[0])
        filepath = item["tags"][1]
        
        if os.path.exists(filepath):
            os.startfile(filepath)
        else:
            messagebox.showerror("错误", "文件不存在，可能已被移动或删除")
    
    def open_folder(self):
        """打开文件所在文件夹"""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = self.file_tree.item(selection[0])
        filepath = item["tags"][1]
        
        if os.path.exists(filepath):
            os.startfile(os.path.dirname(filepath))
        else:
            messagebox.showerror("错误", "文件夹不存在")
    
    def delete_file_record(self):
        """删除文件记录"""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = self.file_tree.item(selection[0])
        file_id = item["tags"][0]
        
        if messagebox.askyesno("确认", "确定要删除此文件记录吗？\n（实际文件不会被删除）"):
            self.pm.cur.execute("DELETE FROM files WHERE id = ?", (file_id,))
            self.pm.conn.commit()
            self.load_files()
            self.update_stats()
    
    def show_file_menu(self, event):
        """显示文件右键菜单"""
        self.file_tree.selection_set(self.file_tree.identify_row(event.y))
        self.file_menu.post(event.x_root, event.y_root)
    
    def do_search(self):
        """搜索"""
        keyword = self.search_var.get().strip()
        if not keyword:
            # 清空并恢复显示
            if self.current_stage_id:
                self.load_files()
            return
        
        results = self.pm.search_files(keyword)
        
        # 显示搜索结果（暂时用对话框展示）
        if results:
            result_text = f"找到 {len(results)} 个结果：\n\n"
            for r in results[:20]:  # 最多显示20条
                result_text += f"📄 {r[0]}\n   项目: {r[3]} / {r[4]}\n   日期: {r[2][:10]}\n\n"
            
            if len(results) > 20:
                result_text += f"... 还有 {len(results)-20} 个结果"
            
            messagebox.showinfo("搜索结果", result_text)
        else:
            messagebox.showinfo("搜索结果", "未找到匹配的文件")
    
    def update_stats(self):
        """更新统计"""
        if not self.current_project_id:
            return
        
        stats = self.pm.get_project_stats(self.current_project_id)
        size_str = self.format_size(stats["total_size"])
        
        stage_info = " | ".join([f"{s[0]}: {s[1]}个" for s in stats["stage_counts"]])
        self.lbl_status.config(text=f"共 {stats['file_count']} 个文件 ({size_str}) | {stage_info}")
    
    @staticmethod
    def format_size(size):
        """格式化文件大小"""
        if size < 1024:
            return f"{size}B"
        elif size < 1024*1024:
            return f"{size/1024:.1f}KB"
        elif size < 1024*1024*1024:
            return f"{size/1024/1024:.1f}MB"
        else:
            return f"{size/1024/1024/1024:.1f}GB"
    
    def smart_archive(self):
        """智能归档 - 选择扫描范围"""
        # 直接弹出选择文件夹对话框
        folder = filedialog.askdirectory(title="选择要扫描的文件夹（选择桌面或任意文件夹）")
        if not folder:
            return
        
        # 直接执行扫描
        self._do_smart_scan([folder], recursive=False)
    
    def _do_smart_scan(self, folders, recursive=False):
        """执行扫描并显示归档建议"""
        files_info = []
        
        for folder in folders:
            if not os.path.exists(folder):
                continue
            
            if recursive:
                for root_dir, dirs, files in os.walk(folder):
                    # 跳过系统文件夹
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['System Volume Information', '$RECYCLE.BIN', 'Windows']]
                    for file in files:
                        filepath = os.path.join(root_dir, file)
                        try:
                            stat = os.stat(filepath)
                            files_info.append({
                                'name': file,
                                'path': filepath,
                                'ext': os.path.splitext(file)[1].lower(),
                                'size': stat.st_size,
                                'mtime': datetime.fromtimestamp(stat.st_mtime),
                                'folder': os.path.basename(root_dir)
                            })
                        except:
                            pass
            else:
                # 只扫描第一层
                try:
                    for item in os.listdir(folder):
                        filepath = os.path.join(folder, item)
                        try:
                            stat = os.stat(filepath)
                            is_dir = os.path.isdir(filepath)
                            files_info.append({
                                'name': ("📂 " if is_dir else "") + item,
                                'path': filepath,
                                'ext': '[文件夹]' if is_dir else os.path.splitext(item)[1].lower(),
                                'size': stat.st_size if not is_dir else 0,
                                'mtime': datetime.fromtimestamp(stat.st_mtime),
                                'folder': os.path.basename(folder)
                            })
                        except:
                            pass
                except:
                    pass
        
        if not files_info:
            messagebox.showinfo("提示", "未找到文件")
            return
        
        # 获取所有项目名称
        all_projects = self.pm.get_all_projects()
        project_names = [p[1] for p in all_projects]
        
        # 为每个文件生成建议
        file_suggestions = self.generate_file_suggestions(files_info)
        
        # ===== 显示确认界面 =====
        dialog = Toplevel(self.root)
        dialog.title(f"智能归档 - 扫描到 {len(files_info)} 个文件/文件夹")
        dialog.geometry("850x620")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 顶部说明
        top_frame = Frame(dialog, bg="#f0f4f8", padx=15, pady=8)
        top_frame.pack(fill=X)
        Label(top_frame, text=f"📂 扫描区域：{', '.join(folders)}", 
              font=("微软雅黑", 9), bg="#f0f4f8", wraplength=800, justify=LEFT).pack(anchor=W)
        Label(top_frame, text="✏️ 双击「建议归档到」列可修改项目  |  点击✓列可取消勾选", 
              font=("微软雅黑", 10), fg="#555", bg="#f0f4f8").pack(anchor=W)
        
        # 表格区域
        table_frame = Frame(dialog)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        scrollbar_y = Scrollbar(table_frame, orient=VERTICAL)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        
        columns = ("check", "filename", "project", "ext", "date")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                            yscrollcommand=scrollbar_y.set,
                            xscrollcommand=scrollbar_x.set)
        tree.heading("check", text="✓")
        tree.heading("filename", text="文件名")
        tree.heading("project", text="建议归档到（双击可修改）")
        tree.heading("ext", text="类型")
        tree.heading("date", text="修改日期")
        tree.column("check", width=40, anchor=CENTER)
        tree.column("filename", width=300)
        tree.column("project", width=230)
        tree.column("ext", width=80, anchor=CENTER)
        tree.column("date", width=90, anchor=CENTER)
        tree.pack(fill=BOTH, expand=True)
        scrollbar_y.config(command=tree.yview)
        scrollbar_x.config(command=tree.xview)
        
        # 填充数据
        row_data = {}
        for f, suggestion in file_suggestions:
            date_str = f['mtime'].strftime("%m-%d") if 'mtime' in f else ""
            item_id = tree.insert("", END, values=("✓", f['name'], suggestion, f.get('ext',''), date_str))
            row_data[item_id] = {'file': f, 'project': suggestion, 'checked': True}
        
        # 双击修改
        def on_double_click(event):
            item = tree.identify_row(event.y)
            col = tree.identify_column(event.x)
            if not item:
                return
            
            if col == "#1":
                data = row_data[item]
                data['checked'] = not data['checked']
                vals = list(tree.item(item, "values"))
                vals[0] = "✓" if data['checked'] else "✗"
                tree.item(item, values=vals)
            
            elif col == "#3":
                edit_dialog = Toplevel(dialog)
                edit_dialog.title("修改归档项目")
                edit_dialog.geometry("350x380")
                edit_dialog.transient(dialog)
                edit_dialog.grab_set()
                edit_dialog.lift()
                
                Label(edit_dialog, text="选择或输入项目名称：", font=("微软雅黑", 11)).pack(padx=15, pady=10, anchor=W)
                var = StringVar(value=row_data[item]['project'].replace("📁 ", ""))
                entry = Entry(edit_dialog, textvariable=var, font=("微软雅黑", 11), width=30)
                entry.pack(padx=15, pady=5)
                
                Label(edit_dialog, text="现有项目：", font=("微软雅黑", 10), fg="gray").pack(padx=15, anchor=W)
                listbox = Listbox(edit_dialog, font=("微软雅黑", 10), height=10)
                listbox.pack(fill=BOTH, expand=True, padx=15, pady=5)
                for pname in project_names:
                    listbox.insert(END, pname)
                
                def select_proj(evt=None):
                    sel = listbox.curselection()
                    if sel:
                        var.set(listbox.get(sel[0]))
                
                listbox.bind("<<ListboxSelect>>", select_proj)
                
                def confirm_proj():
                    new_proj = var.get().strip()
                    if new_proj:
                        row_data[item]['project'] = new_proj
                        vals = list(tree.item(item, "values"))
                        vals[2] = new_proj
                        tree.item(item, values=vals)
                    edit_dialog.destroy()
                
                listbox.bind("<Double-1>", lambda e: confirm_proj())
                Button(edit_dialog, text="确认", font=("微软雅黑", 11), bg="#27ae60", fg="white",
                       command=confirm_proj).pack(pady=8)
        
        tree.bind("<Double-1>", on_double_click)
        
        # 底部固定按钮区域
        bottom_frame = Frame(dialog, bg="#ecf0f1", pady=10)
        bottom_frame.pack(fill=X, side=BOTTOM)
        
        checked_count = len([r for r in row_data.values() if r['checked']])
        lbl_count = Label(bottom_frame, text=f"已选 {checked_count}/{len(files_info)} 个文件", 
                          font=("微软雅黑", 10), fg="#555", bg="#ecf0f1")
        lbl_count.pack(side=LEFT, padx=15)
        
        def do_archive():
            checked_items = [(row_data[iid]['file'], row_data[iid]['project']) 
                           for iid in row_data if row_data[iid]['checked']]
            
            if not checked_items:
                messagebox.showwarning("提示", "没有选中任何文件", parent=dialog)
                return
            
            if not messagebox.askyesno("确认归档", f"确定将 {len(checked_items)} 个文件归档？", parent=dialog):
                return
            
            existing = {p[1]: p[0] for p in self.pm.get_all_projects()}
            project_map = {}
            
            for _, proj_name in checked_items:
                clean_name = proj_name.replace("📁 ", "").replace("📂 ", "").strip()
                if clean_name and clean_name not in project_map:
                    if clean_name in existing:
                        project_map[clean_name] = existing[clean_name]
                    else:
                        try:
                            pid = self.pm.create_project(clean_name, "智能归档自动创建", "智能归档")
                            project_map[clean_name] = pid
                            existing[clean_name] = pid
                        except:
                            pass
            
            success = 0
            for f, proj_name in checked_items:
                clean_name = proj_name.replace("📁 ", "").replace("📂 ", "").strip()
                if clean_name in project_map:
                    try:
                        stages = self.pm.get_project_stages(project_map[clean_name])
                        if stages:
                            self.pm.add_file_to_stage(project_map[clean_name], stages[0][0],
                                                     f['path'], tags="智能归档")
                            success += 1
                    except:
                        pass
            
            dialog.destroy()
            self.load_projects()
            messagebox.showinfo("完成", f"✅ 成功归档 {success}/{len(checked_items)} 个文件！")
        
        Button(bottom_frame, text="取消", font=("微软雅黑", 11), width=10,
               command=dialog.destroy).pack(side=RIGHT, padx=10)
        Button(bottom_frame, text="✅ 确认归档", font=("微软雅黑", 11),
               bg=self.colors["success"], fg="white", width=14,
               command=do_archive).pack(side=RIGHT, padx=5)
    
    def generate_archive_suggestions(self, files_info, ext_count, folder_groups):
        """生成归档建议 - 按项目关键词匹配"""
        suggestions = []
        
        # 获取所有现有项目
        existing_projects = self.pm.get_all_projects()
        project_names = [p[1] for p in existing_projects]
        
        # 分析文件名中的关键词
        keyword_groups = {}
        common_keywords = ['项目', '报告', '方案', '计划', '总结', '会议', '合同', '协议',
                          '设计', '开发', '测试', '验收', '申请', '审批', '通知',
                          '国际化', '课程', '教学', '培训', '研究', '课题',
                          '2024', '2025', '2026', '十五五', '十四五']
        
        for f in files_info:
            filename = f['name'].lower()
            matched = False
            
            # 1. 匹配现有项目名称
            for proj_name in project_names:
                if proj_name.lower() in filename or any(word in filename for word in proj_name.lower().split()):
                    if proj_name not in keyword_groups:
                        keyword_groups[proj_name] = []
                    keyword_groups[proj_name].append(f)
                    matched = True
                    break
            
            # 2. 匹配通用关键词
            if not matched:
                for keyword in common_keywords:
                    if keyword in filename:
                        if keyword not in keyword_groups:
                            keyword_groups[keyword] = []
                        keyword_groups[keyword].append(f)
                        matched = True
                        break
            
            # 3. 按文件夹名分组
            if not matched:
                folder = f['folder']
                if folder not in keyword_groups:
                    keyword_groups[folder] = []
                keyword_groups[folder].append(f)
        
        # 生成建议
        suggestions.append("📁 按项目/主题分类建议：\n")
        
        # 匹配到现有项目的文件
        for proj_name in project_names:
            if proj_name in keyword_groups and len(keyword_groups[proj_name]) > 0:
                count = len(keyword_groups[proj_name])
                suggestions.append(f"   • 「{proj_name}」项目：{count} 个相关文件 → 建议归档到该项目")
        
        # 建议新建项目的分组
        suggestions.append("\n💡 建议新建项目：\n")
        new_project_candidates = []
        for keyword, files in sorted(keyword_groups.items(), key=lambda x: -len(x[1])):
            if keyword not in project_names and len(files) >= 3:
                new_project_candidates.append((keyword, len(files)))
        
        for keyword, count in new_project_candidates[:5]:
            suggestions.append(f"   • 「{keyword}」主题：{count} 个文件 → 建议创建「{keyword}」项目")
        
        # 时间跨度建议
        dates = [f['mtime'] for f in files_info]
        if dates:
            oldest = min(dates)
            newest = max(dates)
            if (newest - oldest).days > 180:
                suggestions.append(f"\n📅 时间跨度 {(newest - oldest).days} 天，建议按时间段细分项目")
        
        if len(suggestions) <= 2:
            suggestions.append("   • 未识别出明显项目关联，建议手动创建项目后归档")
        
        # 保存关键词分组供后续使用
        self._keyword_groups = keyword_groups
        
        return "\n".join(suggestions)
    
    def generate_file_suggestions(self, files_info):
        """为每个文件生成归档建议"""
        suggestions = []
        
        # 获取现有项目名称
        existing_projects = self.pm.get_all_projects()
        project_names = [p[1] for p in existing_projects]
        
        # 常见项目关键词
        common_keywords = ['项目', '报告', '方案', '计划', '总结', '会议', '合同', '协议',
                          '设计', '开发', '测试', '验收', '申请', '审批', '通知',
                          '国际化', '课程', '教学', '培训', '研究', '课题',
                          '海外', '分院', '北柳', '安泰', '泰国', '老挝',
                          '2024', '2025', '2026', '十五五', '十四五']
        
        for f in files_info:
            filename = f['name']
            suggestion = "📁 其他"
            
            # 1. 匹配现有项目
            matched = False
            for proj_name in project_names:
                # 项目名出现在文件名中
                if proj_name.lower() in filename.lower():
                    suggestion = f"📁 {proj_name}"
                    matched = True
                    break
            
            # 2. 匹配关键词
            if not matched:
                for keyword in common_keywords:
                    if keyword.lower() in filename.lower():
                        suggestion = f"📁 {keyword}"
                        matched = True
                        break
            
            # 3. 按文件夹名
            if not matched:
                folder = f['folder']
                if folder and folder not in ['.', '..', '']:
                    suggestion = f"📁 {folder}"
            
            suggestions.append((f, suggestion))
        
        return suggestions
    
    def perform_auto_archive_by_project(self, files_info):
        """执行一键归档 - 按项目关键词"""
        if not hasattr(self, '_keyword_groups') or not self._keyword_groups:
            messagebox.showwarning("提示", "请先进行智能分析")
            return
        
        # 获取现有项目
        existing_projects = {p[1]: p[0] for p in self.pm.get_all_projects()}
        archived_count = 0
        new_projects = []
        
        for keyword, files in sorted(self._keyword_groups.items(), key=lambda x: -len(x[1])):
            if len(files) < 2:  # 少于2个文件跳过
                continue
            
            # 检查是否已有项目
            if keyword in existing_projects:
                project_id = existing_projects[keyword]
            else:
                # 创建新项目
                try:
                    project_id = self.pm.create_project(keyword, f"智能归档创建：{keyword}主题相关文件", "自动归档")
                    new_projects.append(keyword)
                    existing_projects[keyword] = project_id
                except:
                    continue
            
            # 获取第一个阶段ID
            stages = self.pm.get_project_stages(project_id)
            if stages:
                stage_id = stages[0][0]  # 资料收集阶段
                
                # 归档文件
                for f in files:
                    try:
                        self.pm.add_file_to_stage(project_id, stage_id, f['path'], 
                                                 tags="智能归档", note=f"文件名含关键词")
                        archived_count += 1
                    except:
                        pass
        
        self.load_projects()
        
        result_msg = f"按项目归档完成！\n\n"
        result_msg += f"📊 归档统计：\n"
        result_msg += f"   • 共归档 {archived_count} 个文件\n"
        if new_projects:
            result_msg += f"   • 新建 {len(new_projects)} 个项目：\n"
            for p in new_projects[:5]:
                result_msg += f"      - {p}\n"
        
        messagebox.showinfo("完成", result_msg)
    
    def perform_auto_archive_by_type(self, files_info, ext_count):
        """执行一键归档 - 按文件类型"""
        # 定义文件类型分类
        type_groups = {
            '📄 文档': ['.doc', '.docx', '.pdf', '.txt', '.ppt', '.pptx', '.xls', '.xlsx', '.wps'],
            '🖼️ 图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            '🎬 视频': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
            '🎵 音频': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            '💾 压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            '📦 代码': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.go', '.rs'],
        }
        
        # 按类型分组文件
        type_files = {k: [] for k in type_groups.keys()}
        type_files['📁 其他'] = []
        
        for f in files_info:
            ext = f['ext'].lower()
            matched = False
            for type_name, extensions in type_groups.items():
                if ext in extensions:
                    type_files[type_name].append(f)
                    matched = True
                    break
            if not matched:
                type_files['📁 其他'].append(f)
        
        # 获取或创建类型项目
        existing_projects = {p[1]: p[0] for p in self.pm.get_all_projects()}
        archived_count = 0
        created_types = []
        
        for type_name, files in type_files.items():
            if len(files) < 1:
                continue
            
            # 检查是否已有项目
            if type_name in existing_projects:
                project_id = existing_projects[type_name]
            else:
                # 创建新项目
                try:
                    project_id = self.pm.create_project(type_name, f"按文件类型自动归档", "类型归档")
                    created_types.append(type_name)
                    existing_projects[type_name] = project_id
                except:
                    continue
            
            # 获取第一个阶段ID
            stages = self.pm.get_project_stages(project_id)
            if stages:
                stage_id = stages[0][0]
                
                # 归档文件
                for f in files:
                    try:
                        self.pm.add_file_to_stage(project_id, stage_id, f['path'], 
                                                 tags="类型归档", note=f"原始扩展名：{f['ext']}")
                        archived_count += 1
                    except:
                        pass
        
        self.load_projects()
        
        result_msg = f"按类型归档完成！\n\n"
        result_msg += f"📊 归档统计：\n"
        result_msg += f"   • 共归档 {archived_count} 个文件\n"
        result_msg += f"   • 创建/更新 {len(created_types)} 个类型项目：\n"
        for t in created_types:
            count = len(type_files[t])
            result_msg += f"      - {t}: {count} 个文件\n"
        
        messagebox.showinfo("完成", result_msg)

# ==================== 主程序 ====================
def main():
    root = Tk()
    app = ProjectFileManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
