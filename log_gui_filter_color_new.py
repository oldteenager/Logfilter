#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志分析工具 - 超级现代化版本
作者: AI助手
创建时间: 2025年7月10日
功能: 
1. 从日志文件中筛选包含指定关键字的行
2. 显示筛选结果的上下文内容
3. 高亮显示关键字
4. 超级现代化UI界面
5. 深浅主题切换
6. 多文件支持
7. 现代化设计风格
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk, simpledialog
import re
import json
import os
import threading
import time

# 尝试导入超级现代化UI增强器
try:
    from ultra_modern_ui import apply_ultra_modern_ui
    ULTRA_MODERN_UI_AVAILABLE = True
    print("✨ 超级现代化UI增强器已加载")
except ImportError:
    ULTRA_MODERN_UI_AVAILABLE = False
    print("⚠️ 超级现代化UI增强器不可用")

# 尝试导入现代化UI增强器
try:
    from modern_ui_enhancer import apply_modern_ui
    MODERN_UI_AVAILABLE = True
    print("🎨 现代化UI增强器已加载")
except ImportError:
    MODERN_UI_AVAILABLE = False
    print("⚠️ 现代化UI增强器不可用")

# 尝试导入界面美化增强器
try:
    from beauty_enhancer import beautify_app
    BEAUTY_ENHANCER_AVAILABLE = True
    print("💄 界面美化增强器已加载")
except ImportError:
    BEAUTY_ENHANCER_AVAILABLE = False
    print("⚠️ 界面美化增强器不可用")

# 定义高亮颜色配置列表
COLOR_LIST = [
    {'fg': '#000000', 'bg': '#FFFF00'},    # 黑字黄底
    {'fg': '#000000', 'bg': '#00FFFF'},    # 黑字青底
    {'fg': '#FFFFFF', 'bg': '#FF00FF'},    # 白字洋红底
    {'fg': '#FFFFFF', 'bg': '#FF0000'},    # 白字红底
    {'fg': '#FFFFFF', 'bg': '#0000FF'},    # 白字蓝底
    {'fg': '#000000', 'bg': '#FFA500'},    # 黑字橙底
    {'fg': '#FFFFFF', 'bg': '#008000'},    # 白字绿底
    {'fg': '#FFFFFF', 'bg': '#800080'}     # 白字紫底
]

# 定义主题配置
THEMES = {
    'light': {
        'bg': '#FFFFFF',
        'fg': '#000000',
        'select_bg': '#0078D4',
        'select_fg': '#FFFFFF',
        'entry_bg': '#FFFFFF',
        'entry_fg': '#000000',
        'text_bg': '#FFFFFF',
        'text_fg': '#000000',
        'text_select_bg': '#316AC5',
        'button_bg': '#E1E1E1',
        'button_fg': '#000000',
        'button_active_bg': '#CCCCCC',
        'frame_bg': '#F0F0F0',
        'scrollbar_bg': '#F0F0F0',
        'scrollbar_fg': '#C0C0C0',
    },
    'dark': {
        'bg': '#2B2B2B',
        'fg': '#FFFFFF',
        'select_bg': '#0078D4',
        'select_fg': '#FFFFFF',
        'entry_bg': '#3C3C3C',
        'entry_fg': '#FFFFFF',
        'text_bg': '#1E1E1E',
        'text_fg': '#FFFFFF',
        'text_select_bg': '#264F78',
        'button_bg': '#404040',
        'button_fg': '#FFFFFF',
        'button_active_bg': '#505050',
        'frame_bg': '#2B2B2B',
        'scrollbar_bg': '#404040',
        'scrollbar_fg': '#606060',
    }
}

class LogFilterApp:
    """
    日志筛选应用程序主类 - 超级现代化版本
    """
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("🚀 LogMaster Pro - 专业日志分析工具")
        self.root.geometry("1200x800")
        
        # 初始化变量
        self.file_content = []
        self.filtered_results = []
        self.keyword_history = []
        self.tabs = {}
        self.current_tab_id = None
        self.history_file = "search_history.json"  # 历史记录文件
        self.bookmarks_file = "bookmarks.json"  # 书签文件
        self.bookmarks = []  # 书签列表
        
        # 上下文相关变量
        self.context_range = 2  # 默认上下文范围
        self.context_results = []  # 存储带上下文的结果
        self.selected_line_index = None  # 当前选中的行索引
        
        # 筛选配置
        self.case_sensitive = False  # 是否区分大小写
        self.use_regex = False  # 是否使用正则表达式
        self.multiple_keywords = []  # 多关键字搜索
        self.current_keywords = []  # 当前搜索的关键词列表，用于高亮
        
        # 初始化主题
        self.current_theme = 'modern_light' if ULTRA_MODERN_UI_AVAILABLE else 'light'
        self.themes = THEMES.copy()
        
        # 存储需要更新主题的组件
        self.theme_widgets = []
        
        # 创建界面
        self.create_widgets()
        self.apply_theme()
        
        # 应用超级现代化UI增强（优先级最高）
        if ULTRA_MODERN_UI_AVAILABLE:
            self.ui_enhancer = apply_ultra_modern_ui(self)
            print("✨ 超级现代化UI增强已应用")
        # 备选：应用现代化UI增强
        elif MODERN_UI_AVAILABLE:
            self.ui_enhancer = apply_modern_ui(self)
            print("🎨 现代化UI增强已应用")
            
        # 应用界面美化（可叠加）
        if BEAUTY_ENHANCER_AVAILABLE:
            beautify_app(self)
            print("💄 界面美化已应用")
    
    def create_widgets(self):
        """创建主界面"""
        # 创建主容器
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建内容区域
        self.create_content_area()
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_toolbar(self):
        """创建工具栏"""
        self.toolbar = tk.Frame(self.main_frame)
        self.toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # 文件操作按钮
        self.open_button = tk.Button(self.toolbar, text="📁 打开文件", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 高级搜索按钮
        self.advanced_search_button = tk.Button(self.toolbar, text="🔍+ 高级搜索", command=self.show_advanced_search)
        self.advanced_search_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 书签按钮
        self.bookmark_button = tk.Button(self.toolbar, text="🔖 书签", command=self.show_bookmarks)
        self.bookmark_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 导出按钮
        self.export_button = tk.Button(self.toolbar, text="💾 导出", command=self.export_results)
        self.export_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 历史记录管理按钮
        self.history_button = tk.Button(self.toolbar, text="📚 历史", command=self.show_history_manager)
        self.history_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 主题切换按钮
        self.theme_button = tk.Button(self.toolbar, text="🌙 暗黑", command=self.toggle_theme)
        self.theme_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 添加到主题组件列表
        self.theme_widgets.extend([
            ('frame', self.toolbar),
            ('button', self.open_button),
            ('button', self.advanced_search_button),
            ('button', self.bookmark_button),
            ('button', self.export_button),
            ('button', self.history_button),
            ('button', self.theme_button)
        ])
    
    def create_content_area(self):
        """创建内容区域"""
        # 创建搜索框架
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 关键字输入（使用Combobox支持历史记录）
        tk.Label(self.search_frame, text="关键字(逗号分隔):").pack(side=tk.LEFT)
        
        self.keyword_combobox = ttk.Combobox(self.search_frame, width=35)
        self.keyword_combobox.pack(side=tk.LEFT, padx=(5, 5))
        self.keyword_combobox.bind('<Return>', lambda e: self.filter_logs())
        self.keyword_combobox.bind('<Button-1>', self.on_combobox_click)
        
        # 加载历史记录
        self.load_search_history()
        
        # 加载书签
        self.load_bookmarks()
        
        # 添加占位符提示
        placeholder_text = "输入关键字，多个关键字用逗号分隔"
        self.keyword_combobox.set(placeholder_text)
        self.keyword_combobox.bind('<FocusIn>', self.on_combobox_focus_in)
        self.keyword_combobox.bind('<FocusOut>', self.on_combobox_focus_out)
        self.keyword_combobox.config(foreground='gray')
        
        # 保持对原有keyword_entry的兼容性引用
        self.keyword_entry = self.keyword_combobox
        
        # 搜索按钮
        self.search_button = tk.Button(self.search_frame, text="🔍 搜索", command=self.filter_logs)
        self.search_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 上下文范围控制
        tk.Label(self.search_frame, text="上下文:").pack(side=tk.LEFT, padx=(10, 0))
        
        self.context_var = tk.StringVar(value=str(self.context_range))
        self.context_spinbox = tk.Spinbox(self.search_frame, from_=0, to=20, width=5, 
                                         textvariable=self.context_var,
                                         command=self.update_context_range)
        self.context_spinbox.pack(side=tk.LEFT, padx=(5, 5))
        
        # 绑定键盘事件，实现实时更新
        self.context_var.trace('w', self.on_context_change)
        
        # 搜索选项
        self.options_frame = tk.Frame(self.main_frame)
        self.options_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 区分大小写选项
        self.case_var = tk.BooleanVar()
        self.case_check = tk.Checkbutton(self.options_frame, text="区分大小写", 
                                        variable=self.case_var)
        self.case_check.pack(side=tk.LEFT)
        
        # 正则表达式选项
        self.regex_var = tk.BooleanVar()
        self.regex_check = tk.Checkbutton(self.options_frame, text="正则表达式", 
                                         variable=self.regex_var)
        self.regex_check.pack(side=tk.LEFT, padx=(10, 0))
        
        # AND/OR选择选项
        self.logic_var = tk.StringVar(value="OR")  # 默认OR搜索
        tk.Label(self.options_frame, text="多关键词:").pack(side=tk.LEFT, padx=(20, 5))
        self.and_radio = tk.Radiobutton(self.options_frame, text="AND(全匹配)", 
                                       variable=self.logic_var, value="AND")
        self.and_radio.pack(side=tk.LEFT)
        self.or_radio = tk.Radiobutton(self.options_frame, text="OR(任一匹配)", 
                                      variable=self.logic_var, value="OR")
        self.or_radio.pack(side=tk.LEFT, padx=(10, 0))
        
        # 创建左右分割面板
        self.paned_window = tk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：搜索结果列表
        self.left_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, width=400)
        
        tk.Label(self.left_frame, text="📋 搜索结果", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # 结果列表
        self.result_listbox = tk.Listbox(self.left_frame, height=15)
        self.result_listbox.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        self.result_listbox.bind('<<ListboxSelect>>', self.on_result_select)
        
        # 使用Text组件替代Listbox以支持高亮
        self.result_text = tk.Text(self.left_frame, height=15, width=50, wrap=tk.NONE)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        self.result_text.bind('<Button-1>', self.on_result_text_click)
        self.result_text.bind('<Button-3>', self.on_result_text_right_click)  # 右键菜单
        self.result_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 默认显示Text组件，隐藏Listbox
        self.result_listbox.pack_forget()
        self.use_text_display = True  # 标记使用Text显示
        
        # 添加滚动条
        self.listbox_scrollbar = tk.Scrollbar(self.left_frame, orient=tk.VERTICAL)
        self.result_listbox.config(yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command=self.result_listbox.yview)
        
        # 右侧：上下文内容显示
        self.right_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, width=600)
        
        tk.Label(self.right_frame, text="📄 上下文内容", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # 上下文显示区域
        self.context_text = scrolledtext.ScrolledText(self.right_frame, height=15)
        self.context_text.pack(fill=tk.BOTH, expand=True)
        
        # 绑定鼠标事件，实现选中文本高亮相同内容
        self.context_text.bind("<Button-1>", self.on_text_click)
        self.context_text.bind("<B1-Motion>", self.on_text_drag)
        self.context_text.bind("<ButtonRelease-1>", self.on_text_release)
        
        # 添加到主题组件列表
        self.theme_widgets.extend([
            ('frame', self.search_frame),
            ('combobox', self.keyword_combobox),
            ('button', self.search_button),
            ('frame', self.options_frame),
            ('text', self.context_text),
            ('listbox', self.result_listbox),
            ('text', self.result_text)
        ])
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = tk.Frame(self.main_frame)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(self.status_bar, text="就绪", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT)
        
        # 添加到主题组件列表
        self.theme_widgets.extend([
            ('frame', self.status_bar),
            ('label', self.status_label)
        ])
        
    def update_context_range(self):
        """更新上下文范围 - 实时调整显示，保持视图位置"""
        try:
            new_range = int(self.context_var.get())
            if new_range != self.context_range:
                self.context_range = new_range
                # 实时更新上下文显示，保持视图位置不跳动
                if self.selected_line_index is not None:
                    self.show_context(self.selected_line_index, preserve_view=True)
        except ValueError:
            # 如果输入无效，恢复到之前的值
            self.context_var.set(str(self.context_range))
    
    def on_result_select(self, event):
        """处理结果列表选择事件"""
        selection = self.result_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_line_index = index
            self.show_context(index)
    
    def show_context(self, result_index, preserve_view=False):
        """显示选中结果的上下文 - 支持保持视图位置"""
        if not self.filtered_results or result_index >= len(self.filtered_results):
            return
        
        line_num, _ = self.filtered_results[result_index]
        
        # 如果需要保持视图，先保存当前滚动位置和光标位置
        current_scroll_fraction = None
        target_line_relative_pos = None
        
        if preserve_view:
            try:
                # 保存当前滚动位置（相对于总内容的比例）
                scroll_info = self.context_text.yview()
                current_scroll_fraction = scroll_info[0]
                
                # 查找当前目标行在视图中的相对位置
                content = self.context_text.get(1.0, tk.END)
                lines = content.split('\n')
                total_lines = len([l for l in lines if l.strip()])
                
                for i, line in enumerate(lines):
                    if line.startswith('>>>'):
                        target_line_relative_pos = i / max(1, total_lines - 1)
                        break
                        
            except Exception as e:
                print(f"保存视图状态失败: {e}")
        
        # 计算上下文范围
        start_line = max(0, line_num - 1 - self.context_range)
        end_line = min(len(self.file_content), line_num + self.context_range)
        
        # 清空上下文显示区域
        self.context_text.delete(1.0, tk.END)
        
        # 显示上下文
        target_line_index = None  # 记录目标行在新内容中的位置
        context_lines = []
        
        for i in range(start_line, end_line):
            line_content = self.file_content[i].rstrip()
            line_number = i + 1
            
            # 标记目标行
            if line_number == line_num:
                line_display = f">>> [{line_number:4d}] {line_content}\n"
                target_line_index = len(context_lines) + 1  # 在新内容中的行号（1-based）
            else:
                line_display = f"    [{line_number:4d}] {line_content}\n"
            
            context_lines.append(line_display)
            self.context_text.insert(tk.END, line_display)
        
        # 高亮关键字
        self.highlight_context_keywords()
        
        # 如果需要保持视图位置，尝试智能恢复
        if preserve_view and target_line_index:
            try:
                self.context_text.update_idletasks()  # 确保内容已经渲染
                
                new_total_lines = len(context_lines)
                if new_total_lines > 1:
                    # 计算目标行在新内容中的相对位置
                    new_target_relative_pos = (target_line_index - 1) / max(1, new_total_lines - 1)
                    
                    # 如果有之前的目标行位置信息，尝试保持相同的相对位置
                    if target_line_relative_pos is not None:
                        # 计算滚动偏移，让目标行保持在视图中相似的位置
                        visible_height = self.context_text.winfo_height()
                        line_height = self.context_text.dlineinfo("1.0")
                        if line_height:
                            lines_per_view = visible_height / line_height[3]
                            target_view_position = target_line_relative_pos * lines_per_view
                            desired_scroll_top = max(0, (target_line_index - target_view_position) / new_total_lines)
                            self.context_text.yview_moveto(desired_scroll_top)
                        else:
                            # 如果无法计算行高，使用简单策略
                            scroll_pos = max(0, new_target_relative_pos - 0.3)
                            self.context_text.yview_moveto(scroll_pos)
                    else:
                        # 没有之前的位置信息，让目标行居中
                        scroll_pos = max(0, new_target_relative_pos - 0.4)
                        self.context_text.yview_moveto(scroll_pos)
                
            except Exception as e:
                print(f"恢复视图位置失败: {e}")
                # 如果恢复失败，至少确保目标行可见
                if target_line_index:
                    self.context_text.see(f"{target_line_index}.0")
        else:
            # 不需要保持视图，正常滚动到目标行
            if target_line_index:
                self.context_text.see(f"{target_line_index}.0")
    
    def highlight_context_keywords(self):
        """在上下文中高亮关键字 - 增强版本"""
        try:
            # 获取当前搜索的关键词
            if not hasattr(self, 'current_keywords') or not self.current_keywords:
                return
            
            # 获取搜索选项
            case_sensitive = getattr(self, 'case_var', tk.BooleanVar()).get()
            
            # 清除之前的高亮
            self.context_text.tag_remove("highlight", "1.0", tk.END)
            self.context_text.tag_remove("target_line", "1.0", tk.END)
            
            # 清除之前的关键词高亮标签
            for i in range(len(COLOR_LIST)):
                self.context_text.tag_remove(f"keyword_{i}", "1.0", tk.END)
            
            # 高亮目标行（以>>>开头的行）
            start_pos = "1.0"
            while True:
                pos = self.context_text.search(">>>", start_pos, tk.END)
                if not pos:
                    break
                
                # 高亮整行
                line_start = f"{pos.split('.')[0]}.0"
                line_end = f"{pos.split('.')[0]}.end"
                self.context_text.tag_add("target_line", line_start, line_end)
                start_pos = f"{int(pos.split('.')[0]) + 1}.0"
            
            # 高亮每个关键词（使用不同颜色）
            for keyword_idx, keyword in enumerate(self.current_keywords):
                if not keyword:
                    continue
                
                color_idx = keyword_idx % len(COLOR_LIST)
                tag_name = f"keyword_{keyword_idx}"
                
                start_pos = "1.0"
                while True:
                    pos = self.context_text.search(keyword, start_pos, tk.END, 
                                                  nocase=not case_sensitive)
                    if not pos:
                        break
                    
                    end_pos = f"{pos}+{len(keyword)}c"
                    self.context_text.tag_add(tag_name, pos, end_pos)
                    start_pos = end_pos
                
                # 配置关键词高亮样式
                self.context_text.tag_configure(tag_name, 
                    background=COLOR_LIST[color_idx]['bg'], 
                    foreground=COLOR_LIST[color_idx]['fg'])
            
            # 配置目标行高亮样式
            self.context_text.tag_configure("target_line", 
                background="#FFE4B5",  # 淡橙色背景
                foreground="#8B4513")  # 深棕色文字
            
        except Exception as e:
            print(f"上下文高亮失败: {e}")
    
    def open_file(self):
        """打开文件"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择日志文件",
                filetypes=[
                    ("日志文件", "*.log"),
                    ("文本文件", "*.txt"),
                    ("所有文件", "*.*")
                ]
            )
            
            if file_path:
                # 保存当前文件路径
                self.current_file_path = file_path
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    self.file_content = file.readlines()
                
                self.status_label.config(text=f"已加载文件: {os.path.basename(file_path)} ({len(self.file_content)} 行)")
                
                # 清空搜索结果和上下文显示
                self.result_listbox.delete(0, tk.END)
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.context_text.delete(1.0, tk.END)
                
                # 显示提示信息
                self.result_listbox.insert(tk.END, "文件已加载，请输入关键字进行搜索...")
                self.result_text.insert(tk.END, "文件已加载，请输入关键字进行搜索...")
                self.context_text.insert(tk.END, "文件已加载，请输入关键字进行搜索...")
                self.result_text.config(state=tk.DISABLED)
                
        except Exception as e:
            messagebox.showerror("错误", f"打开文件失败: {str(e)}")
    
    def filter_logs(self):
        """筛选日志 - 增强版本，支持逗号分隔多关键词"""
        keyword_input = self.keyword_entry.get().strip()
        
        print(f"🔍 开始搜索，原始输入: '{keyword_input}'")
        
        # 检查是否为占位符文本或空输入
        placeholder_text = "输入关键字，多个关键字用逗号分隔"
        if not keyword_input or keyword_input == placeholder_text:
            print("❌ 输入为空或为占位符文本")
            messagebox.showwarning("警告", "请输入关键字")
            # 确保占位符文本正确显示
            if keyword_input != placeholder_text:
                self.keyword_entry.delete(0, tk.END)
                self.keyword_entry.insert(0, placeholder_text)
                self.keyword_entry.config(fg='gray')
            return
        
        if not self.file_content:
            print("❌ 没有加载文件")
            messagebox.showwarning("警告", "请先打开文件")
            return
        
        try:
            # 获取搜索选项
            case_sensitive = self.case_var.get()
            use_regex = self.regex_var.get()
            search_logic = self.logic_var.get()  # 获取AND/OR选择
            
            # 解析多关键词（逗号分隔）
            keywords = [k.strip() for k in keyword_input.split(',') if k.strip()]
            if not keywords:
                messagebox.showwarning("警告", "请输入有效的关键字")
                return
            
            # 调试信息
            print(f"🔍 搜索关键词: {keywords}")
            print(f"📋 关键词数量: {len(keywords)}")
            print(f"🔗 搜索逻辑: {search_logic}")
            
            # 存储当前搜索的关键词，用于高亮
            self.current_keywords = keywords
            
            # 筛选包含关键字的行
            self.filtered_results = []
            
            for i, line in enumerate(self.file_content):
                line_content = line.strip()
                found = False
                
                if use_regex:
                    # 正则表达式搜索
                    try:
                        flags = 0 if case_sensitive else re.IGNORECASE
                        if search_logic == "AND":
                            found = all(re.search(keyword, line_content, flags) for keyword in keywords)
                        else:  # OR
                            found = any(re.search(keyword, line_content, flags) for keyword in keywords)
                    except re.error as e:
                        messagebox.showerror("正则表达式错误", f"正则表达式语法错误: {e}")
                        return
                else:
                    # 普通文本搜索
                    search_line = line_content if case_sensitive else line_content.lower()
                    search_keywords = keywords if case_sensitive else [k.lower() for k in keywords]
                    
                    if search_logic == "AND":
                        # 所有关键词都需要匹配
                        found = all(search_keyword in search_line for search_keyword in search_keywords)
                    else:  # OR
                        # 任意一个关键词匹配即可
                        found = any(search_keyword in search_line for search_keyword in search_keywords)
                    
                    # 调试信息
                    if found:
                        print(f"✅ 匹配第 {i+1} 行: {line_content[:50]}...")
                    elif i < 5:  # 只显示前5行的调试信息
                        if search_logic == "AND":
                            missing_keywords = [k for k in search_keywords if k not in search_line]
                            print(f"❌ 第 {i+1} 行不匹配，缺少关键词: {missing_keywords}")
                        else:
                            print(f"❌ 第 {i+1} 行不匹配，无任何关键词")
                
                if found:
                    self.filtered_results.append((i + 1, line_content))
            
            print(f"🎯 总共找到 {len(self.filtered_results)} 条匹配结果")
            
            # 显示结果
            self.display_results(keyword_input)
            
            # 更新状态
            self.status_label.config(text=f"找到 {len(self.filtered_results)} 条匹配结果 (关键词: {len(keywords)}个, {search_logic}模式)")
            
            # 添加到历史记录
            self.add_to_search_history(keyword_input)
            
        except Exception as e:
            messagebox.showerror("错误", f"筛选失败: {str(e)}")
    
    def display_results(self, keyword):
        """显示筛选结果 - 增强版本，支持关键字高亮"""
        # 清空之前的结果
        self.result_listbox.delete(0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.context_text.delete(1.0, tk.END)
        
        if not self.filtered_results:
            # 显示无结果信息
            no_result_msg = f"未找到匹配的结果 (关键词: {keyword})"
            detail_msg = """请检查:
1. 关键词是否正确
2. 是否区分大小写
3. 文件是否包含相关内容"""
            
            self.result_listbox.insert(tk.END, no_result_msg)
            self.result_text.insert(tk.END, no_result_msg + "\n\n" + detail_msg)
            self.context_text.insert(tk.END, detail_msg)
            self.result_text.config(state=tk.DISABLED)
            
            # 更新状态栏
            self.status_label.config(text=f"未找到匹配结果 - 关键词: {keyword}")
            return
        
        # 显示找到的结果数量
        result_count_msg = f"找到 {len(self.filtered_results)} 条匹配结果:\n" + "="*40 + "\n"
        self.result_text.insert(tk.END, result_count_msg)
        
        # 在结果列表中显示所有匹配的行
        for i, (line_num, line_content) in enumerate(self.filtered_results):
            # 为listbox添加内容（保持兼容性）
            display_text = f"[{line_num:4d}] {line_content[:80]}{'...' if len(line_content) > 80 else ''}"
            self.result_listbox.insert(tk.END, display_text)
            
            # 为Text组件添加内容，添加行号以便点击识别
            self.result_text.insert(tk.END, f"{display_text}\n")
        
        # 高亮搜索结果中的关键字（在设置为只读之前）
        self.highlight_result_keywords()
        
        # 设置为只读
        self.result_text.config(state=tk.DISABLED)
        
        # 默认选中第一个结果
        if self.filtered_results:
            self.result_listbox.selection_set(0)
            self.selected_line_index = 0
            self.show_context(0)
            self.highlight_selected_result_line(0)

    def highlight_result_keywords(self):
        """高亮搜索结果中的关键字"""
        try:
            if not hasattr(self, 'current_keywords') or not self.current_keywords:
                return
            
            # 获取搜索选项
            case_sensitive = getattr(self, 'case_var', tk.BooleanVar()).get()
            
            # 暂时设置为可编辑状态
            self.result_text.config(state=tk.NORMAL)
            
            # 清除之前的关键词高亮标签
            for i in range(len(COLOR_LIST)):
                self.result_text.tag_remove(f"result_keyword_{i}", "1.0", tk.END)
            
            # 高亮每个关键词（使用不同颜色）
            for keyword_idx, keyword in enumerate(self.current_keywords):
                if not keyword:
                    continue
                
                color_idx = keyword_idx % len(COLOR_LIST)
                tag_name = f"result_keyword_{keyword_idx}"
                
                start_pos = "1.0"
                while True:
                    pos = self.result_text.search(keyword, start_pos, tk.END, 
                                                 nocase=not case_sensitive)
                    if not pos:
                        break
                    
                    end_pos = f"{pos}+{len(keyword)}c"
                    self.result_text.tag_add(tag_name, pos, end_pos)
                    start_pos = end_pos
                
                # 配置关键词高亮样式
                self.result_text.tag_configure(tag_name, 
                    background=COLOR_LIST[color_idx]['bg'], 
                    foreground=COLOR_LIST[color_idx]['fg'])
            
            # 恢复为只读状态
            self.result_text.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"搜索结果高亮失败: {e}")
            self.result_text.config(state=tk.DISABLED)
    
    def highlight_keywords(self, keyword):
        """高亮关键字 - 已弃用，功能已整合到highlight_context_keywords中"""
        # 这个方法已经不再使用，因为高亮功能已经整合到上下文显示中
        # 保留此方法以防止调用错误
        pass
    
    def toggle_theme(self):
        """切换主题"""
        # 支持超级现代化UI主题
        if ULTRA_MODERN_UI_AVAILABLE and hasattr(self, 'ui_enhancer'):
            if self.current_theme in ['light', 'modern_light']:
                self.current_theme = 'modern_dark'
            else:
                self.current_theme = 'modern_light'
        else:
            # 传统主题切换
            self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        
        self.apply_theme()
    
    def apply_theme(self):
        """应用主题样式"""
        # 使用实例的themes属性，如果当前主题不存在则回退到全局THEMES
        if self.current_theme in self.themes:
            theme = self.themes[self.current_theme]
        else:
            theme = THEMES.get(self.current_theme, THEMES['light'])
        
        # 更新主题切换按钮文本
        if hasattr(self, 'theme_button'):
            if ULTRA_MODERN_UI_AVAILABLE:
                self.theme_button.config(text="☀️ 明亮" if self.current_theme == 'modern_dark' else "🌙 暗黑")
            else:
                self.theme_button.config(text="☀️ 明亮" if self.current_theme == 'dark' else "🌙 暗黑")
        
        # 更新所有组件的主题
        for widget_type, widget in self.theme_widgets:
            try:
                if widget_type == 'frame':
                    widget.config(bg=theme.get('frame_bg', theme['bg']))
                elif widget_type == 'label':
                    widget.config(bg=theme['bg'], fg=theme['fg'])
                elif widget_type == 'entry':
                    widget.config(bg=theme['entry_bg'], fg=theme['entry_fg'], 
                                insertbackground=theme['fg'])
                elif widget_type == 'combobox':
                    # TTK Combobox需要使用style来设置主题
                    style = ttk.Style()
                    style.configure('TCombobox', 
                                  fieldbackground=theme['entry_bg'],
                                  background=theme['button_bg'],
                                  foreground=theme['entry_fg'])
                elif widget_type == 'button':
                    widget.config(bg=theme['button_bg'], fg=theme['button_fg'],
                                activebackground=theme['button_active_bg'])
                elif widget_type == 'text':
                    widget.config(bg=theme['text_bg'], fg=theme['text_fg'],
                                selectbackground=theme['text_select_bg'],
                                selectforeground=theme['select_fg'],
                                insertbackground=theme['fg'])
                elif widget_type == 'listbox':
                    widget.config(bg=theme['text_bg'], fg=theme['text_fg'],
                                selectbackground=theme['text_select_bg'],
                                selectforeground=theme['select_fg'])
            except Exception as e:
                print(f"主题应用失败 {widget_type}: {e}")
        
        # 更新根窗口背景
        self.root.config(bg=theme['bg'])
    
    def get_current_theme(self):
        """获取当前主题配置"""
        if self.current_theme in self.themes:
            return self.themes[self.current_theme]
        else:
            return THEMES.get(self.current_theme, THEMES['light'])

    def show_advanced_search(self):
        """显示高级搜索对话框"""
        try:
            search_window = tk.Toplevel(self.root)
            search_window.title("🔍+ 高级搜索")
            search_window.geometry("500x400")
            search_window.transient(self.root)
            search_window.grab_set()
            
            theme = self.get_current_theme()
            search_window.configure(bg=theme['bg'])
            
            # 多关键字搜索
            tk.Label(search_window, text="多关键字搜索 (每行一个):", 
                    bg=theme['bg'], fg=theme['fg']).pack(anchor=tk.W, padx=10, pady=5)
            
            keywords_text = tk.Text(search_window, height=8, width=50)
            keywords_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
            
            # 搜索选项
            options_frame = tk.Frame(search_window, bg=theme['bg'])
            options_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # AND/OR选择
            logic_var = tk.StringVar(value="OR")
            tk.Label(options_frame, text="逻辑关系:", bg=theme['bg'], fg=theme['fg']).pack(side=tk.LEFT)
            tk.Radiobutton(options_frame, text="AND (全部包含)", variable=logic_var, value="AND",
                          bg=theme['bg'], fg=theme['fg']).pack(side=tk.LEFT, padx=5)
            tk.Radiobutton(options_frame, text="OR (任一包含)", variable=logic_var, value="OR",
                          bg=theme['bg'], fg=theme['fg']).pack(side=tk.LEFT, padx=5)
            
            # 按钮
            button_frame = tk.Frame(search_window, bg=theme['bg'])
            button_frame.pack(fill=tk.X, padx=10, pady=10)
            
            def do_advanced_search():
                keywords = [k.strip() for k in keywords_text.get(1.0, tk.END).split('\n') if k.strip()]
                if keywords:
                    self.advanced_filter_logs(keywords, logic_var.get())
                    search_window.destroy()
            
            tk.Button(button_frame, text="🔍 搜索", command=do_advanced_search).pack(side=tk.LEFT)
            tk.Button(button_frame, text="❌ 取消", command=search_window.destroy).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("错误", f"打开高级搜索失败: {str(e)}")
    
    def advanced_filter_logs(self, keywords, logic="OR"):
        """高级多关键字筛选"""
        if not self.file_content:
            messagebox.showwarning("警告", "请先打开文件")
            return
        
        try:
            self.filtered_results = []
            case_sensitive = getattr(self, 'case_var', tk.BooleanVar()).get()
            
            for i, line in enumerate(self.file_content):
                line_content = line.strip()
                search_line = line_content if case_sensitive else line_content.lower()
                
                if logic == "AND":
                    # 所有关键字都必须包含
                    found = all(
                        (k if case_sensitive else k.lower()) in search_line 
                        for k in keywords
                    )
                else:  # OR
                    # 任一关键字包含即可
                    found = any(
                        (k if case_sensitive else k.lower()) in search_line 
                        for k in keywords
                    )
                
                if found:
                    self.filtered_results.append((i + 1, line_content))
            
            # 显示结果
            self.display_results(", ".join(keywords))
            self.status_label.config(text=f"找到 {len(self.filtered_results)} 条匹配结果 ({logic})")
            
        except Exception as e:
            messagebox.showerror("错误", f"高级搜索失败: {str(e)}")
    
    def show_bookmarks(self):
        """显示书签管理窗口"""
        try:
            bookmark_window = tk.Toplevel(self.root)
            bookmark_window.title("🔖 书签管理")
            bookmark_window.geometry("700x600")
            bookmark_window.transient(self.root)
            bookmark_window.grab_set()
            
            theme = self.get_current_theme()
            bookmark_window.configure(bg=theme['bg'])
            
            # 标题栏
            title_frame = tk.Frame(bookmark_window, bg=theme['bg'])
            title_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(title_frame, text="书签管理", font=('Arial', 14, 'bold'),
                    bg=theme['bg'], fg=theme['fg']).pack(side=tk.LEFT)
            
            count_label = tk.Label(title_frame, text=f"共 {len(self.bookmarks)} 个书签",
                                  bg=theme['bg'], fg=theme['fg'])
            count_label.pack(side=tk.RIGHT)
            
            # 添加书签区域
            add_frame = tk.Frame(bookmark_window, bg=theme['bg'])
            add_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            tk.Label(add_frame, text="添加当前搜索为书签:", 
                    bg=theme['bg'], fg=theme['fg']).pack(anchor=tk.W)
            
            add_input_frame = tk.Frame(add_frame, bg=theme['bg'])
            add_input_frame.pack(fill=tk.X, pady=(5, 0))
            
            tk.Label(add_input_frame, text="名称:", 
                    bg=theme['bg'], fg=theme['fg']).pack(side=tk.LEFT)
            
            bookmark_name_entry = tk.Entry(add_input_frame, width=30)
            bookmark_name_entry.pack(side=tk.LEFT, padx=(5, 5))
            
            def add_current_bookmark():
                name = bookmark_name_entry.get().strip()
                if not name:
                    messagebox.showwarning("警告", "请输入书签名称")
                    return
                
                current_search = self.keyword_entry.get().strip()
                placeholder_text = "输入关键字，多个关键字用逗号分隔"
                
                if not current_search or current_search == placeholder_text:
                    messagebox.showwarning("警告", "没有当前搜索内容可保存")
                    return
                
                bookmark = {
                    'name': name,
                    'keywords': current_search,
                    'case_sensitive': self.case_var.get(),
                    'use_regex': self.regex_var.get(),
                    'search_logic': self.logic_var.get(),
                    'context_range': self.context_range,
                    'created_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'file_info': os.path.basename(getattr(self, 'current_file_path', '未知文件')) if hasattr(self, 'current_file_path') else '未知文件'
                }
                
                self.add_bookmark(bookmark)
                bookmark_name_entry.delete(0, tk.END)
                
                # 刷新列表
                refresh_bookmark_list()
                count_label.config(text=f"共 {len(self.bookmarks)} 个书签")
                
                messagebox.showinfo("成功", f"书签 '{name}' 已添加")
            
            tk.Button(add_input_frame, text="➕ 添加", command=add_current_bookmark,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.LEFT, padx=(0, 5))
            
            # 书签列表
            list_frame = tk.Frame(bookmark_window, bg=theme['bg'])
            list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            tk.Label(list_frame, text="已保存的书签:", 
                    bg=theme['bg'], fg=theme['fg']).pack(anchor=tk.W)
            
            # 创建Treeview来显示书签详细信息
            columns = ('名称', '关键字', '选项', '创建时间')
            self.bookmark_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
            
            # 设置列标题和宽度
            self.bookmark_tree.heading('名称', text='书签名称')
            self.bookmark_tree.heading('关键字', text='搜索关键字')
            self.bookmark_tree.heading('选项', text='搜索选项')
            self.bookmark_tree.heading('创建时间', text='创建时间')
            
            self.bookmark_tree.column('名称', width=120)
            self.bookmark_tree.column('关键字', width=200)
            self.bookmark_tree.column('选项', width=150)
            self.bookmark_tree.column('创建时间', width=130)
            
            # 添加滚动条
            tree_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.bookmark_tree.yview)
            self.bookmark_tree.configure(yscrollcommand=tree_scrollbar.set)
            
            self.bookmark_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            def refresh_bookmark_list():
                """刷新书签列表"""
                for item in self.bookmark_tree.get_children():
                    self.bookmark_tree.delete(item)
                
                for i, bookmark in enumerate(self.bookmarks):
                    options = []
                    if bookmark.get('case_sensitive', False):
                        options.append('区分大小写')
                    if bookmark.get('use_regex', False):
                        options.append('正则表达式')
                    options.append(f"{bookmark.get('search_logic', 'OR')}搜索")
                    options.append(f"上下文{bookmark.get('context_range', 2)}")
                    
                    self.bookmark_tree.insert('', 'end', values=(
                        bookmark['name'],
                        bookmark['keywords'][:30] + ('...' if len(bookmark['keywords']) > 30 else ''),
                        ', '.join(options),
                        bookmark.get('created_time', '未知')
                    ))
            
            refresh_bookmark_list()
            
            # 按钮区域
            button_frame = tk.Frame(bookmark_window, bg=theme['bg'])
            button_frame.pack(fill=tk.X, padx=10, pady=10)
            
            def use_selected_bookmark():
                """使用选中的书签"""
                selection = self.bookmark_tree.selection()
                if not selection:
                    messagebox.showwarning("提示", "请先选择一个书签")
                    return
                
                item = selection[0]
                index = self.bookmark_tree.index(item)
                
                if index < len(self.bookmarks):
                    bookmark = self.bookmarks[index]
                    
                    # 应用书签设置
                    self.keyword_combobox.set(bookmark['keywords'])
                    self.keyword_combobox.config(foreground='black')
                    self.case_var.set(bookmark.get('case_sensitive', False))
                    self.regex_var.set(bookmark.get('use_regex', False))
                    self.logic_var.set(bookmark.get('search_logic', 'OR'))
                    
                    context_range = bookmark.get('context_range', 2)
                    self.context_var.set(str(context_range))
                    self.context_range = context_range
                    
                    bookmark_window.destroy()
                    
                    # 提示用户
                    messagebox.showinfo("书签已应用", 
                                      f"已应用书签 '{bookmark['name']}'，请点击搜索按钮开始搜索")
            
            def delete_selected_bookmark():
                """删除选中的书签"""
                selection = self.bookmark_tree.selection()
                if not selection:
                    messagebox.showwarning("提示", "请先选择一个书签")
                    return
                
                item = selection[0]
                index = self.bookmark_tree.index(item)
                
                if index < len(self.bookmarks):
                    bookmark_name = self.bookmarks[index]['name']
                    result = messagebox.askyesno("确认删除", f"确定要删除书签 '{bookmark_name}' 吗？")
                    
                    if result:
                        self.bookmarks.pop(index)
                        self.save_bookmarks()
                        refresh_bookmark_list()
                        count_label.config(text=f"共 {len(self.bookmarks)} 个书签")
                        messagebox.showinfo("完成", f"书签 '{bookmark_name}' 已删除")
            
            def export_bookmarks():
                """导出书签"""
                if not self.bookmarks:
                    messagebox.showinfo("提示", "没有书签可导出")
                    return
                
                file_path = filedialog.asksaveasfilename(
                    title="导出书签",
                    defaultextension=".json",
                    filetypes=[
                        ("JSON文件", "*.json"),
                        ("文本文件", "*.txt"),
                        ("所有文件", "*.*")
                    ]
                )
                
                if file_path:
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            if file_path.endswith('.json'):
                                json.dump(self.bookmarks, f, ensure_ascii=False, indent=2)
                            else:
                                f.write("日志分析工具 - 书签导出\n")
                                f.write("=" * 50 + "\n\n")
                                for i, bookmark in enumerate(self.bookmarks, 1):
                                    f.write(f"{i}. {bookmark['name']}\n")
                                    f.write(f"   关键字: {bookmark['keywords']}\n")
                                    f.write(f"   创建时间: {bookmark.get('created_time', '未知')}\n")
                                    f.write(f"   搜索选项: 区分大小写={bookmark.get('case_sensitive', False)}, ")
                                    f.write(f"正则表达式={bookmark.get('use_regex', False)}, ")
                                    f.write(f"搜索逻辑={bookmark.get('search_logic', 'OR')}\n")
                                    f.write(f"   上下文范围: {bookmark.get('context_range', 2)}\n\n")
                        
                        messagebox.showinfo("导出成功", f"书签已导出到: {file_path}")
                    except Exception as e:
                        messagebox.showerror("导出失败", f"导出书签失败: {str(e)}")
            
            def import_bookmarks():
                """导入书签"""
                file_path = filedialog.askopenfilename(
                    title="导入书签",
                    filetypes=[
                        ("JSON文件", "*.json"),
                        ("所有文件", "*.*")
                    ]
                )
                
                if file_path:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            imported_bookmarks = json.load(f)
                        
                        if not isinstance(imported_bookmarks, list):
                            messagebox.showerror("导入失败", "无效的书签文件格式")
                            return
                        
                        # 验证书签格式
                        valid_bookmarks = []
                        for bookmark in imported_bookmarks:
                            if isinstance(bookmark, dict) and 'name' in bookmark and 'keywords' in bookmark:
                                valid_bookmarks.append(bookmark)
                        
                        if not valid_bookmarks:
                            messagebox.showerror("导入失败", "文件中没有有效的书签")
                            return
                        
                        # 合并书签（避免重复）
                        existing_names = {b['name'] for b in self.bookmarks}
                        new_count = 0
                        
                        for bookmark in valid_bookmarks:
                            if bookmark['name'] not in existing_names:
                                self.bookmarks.append(bookmark)
                                existing_names.add(bookmark['name'])
                                new_count += 1
                        
                        self.save_bookmarks()
                        refresh_bookmark_list()
                        count_label.config(text=f"共 {len(self.bookmarks)} 个书签")
                        
                        messagebox.showinfo("导入成功", f"成功导入 {new_count} 个新书签")
                        
                    except Exception as e:
                        messagebox.showerror("导入失败", f"导入书签失败: {str(e)}")
            
            # 按钮布局
            tk.Button(button_frame, text="✅ 使用选中", command=use_selected_bookmark,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Button(button_frame, text="🗑️ 删除选中", command=delete_selected_bookmark,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Button(button_frame, text="📤 导出书签", command=export_bookmarks,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Button(button_frame, text="📥 导入书签", command=import_bookmarks,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Button(button_frame, text="❌ 关闭", command=bookmark_window.destroy,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.RIGHT)
            
            # 双击使用书签
            def on_double_click(event):
                use_selected_bookmark()
            
            self.bookmark_tree.bind('<Double-1>', on_double_click)
            
            # 使用说明
            help_frame = tk.Frame(bookmark_window, bg=theme['bg'])
            help_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            help_text = "💡 提示: 双击书签可直接使用，书签会保存搜索条件和选项设置"
            tk.Label(help_frame, text=help_text, font=('Arial', 9),
                    bg=theme['bg'], fg=theme['fg']).pack()
            
        except Exception as e:
            messagebox.showerror("错误", f"打开书签管理失败: {str(e)}")
    
    def export_results(self):
        """导出搜索结果"""
        if not self.filtered_results:
            messagebox.showwarning("警告", "没有搜索结果可导出")
            return
        
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="导出搜索结果",
                defaultextension=".txt",
                filetypes=[
                    ("文本文件", "*.txt"),
                    ("CSV文件", "*.csv"),
                    ("所有文件", "*.*")
                ]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"搜索结果导出\n")
                    f.write(f"关键字: {self.keyword_entry.get()}\n")
                    f.write(f"匹配数量: {len(self.filtered_results)}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for line_num, line_content in self.filtered_results:
                        f.write(f"[第{line_num}行] {line_content}\n")
                
                messagebox.showinfo("导出成功", f"结果已导出到: {file_path}")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

    def on_text_click(self, event):
        """鼠标点击事件处理"""
        # 记录点击位置
        self.click_pos = self.context_text.index(tk.INSERT)
    
    def on_text_drag(self, event):
        """鼠标拖拽事件处理"""
        pass  # 暂时不需要处理
    
    def on_text_release(self, event):
        """鼠标释放事件处理 - 高亮选中的相同文本"""
        try:
            # 获取选中的文本
            selected_text = self.context_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text and len(selected_text.strip()) > 0:
                self.highlight_selected_text(selected_text.strip())
        except tk.TclError:
            # 没有选中文本，清除高亮
            self.clear_selected_highlight()
    
    def highlight_selected_text(self, selected_text):
        """高亮选中的文本在整个上下文中的所有出现"""
        try:
            # 清除之前的选中高亮
            self.context_text.tag_remove("selected_highlight", "1.0", tk.END)
            
            # 如果选中文本太短，不进行高亮
            if len(selected_text) < 2:
                return
            
            # 搜索并高亮所有匹配的文本
            start_pos = "1.0"
            while True:
                pos = self.context_text.search(selected_text, start_pos, tk.END)
                if not pos:
                    break
                
                end_pos = f"{pos}+{len(selected_text)}c"
                self.context_text.tag_add("selected_highlight", pos, end_pos)
                start_pos = end_pos
            
            # 配置高亮样式（使用醒目的颜色）
            self.context_text.tag_configure("selected_highlight", 
                background="#FF69B4",  # 热粉色背景
                foreground="#FFFFFF")  # 白色文字
            
        except Exception as e:
            print(f"选中文本高亮失败: {e}")
    
    def clear_selected_highlight(self):
        """清除选中文本的高亮"""
        try:
            self.context_text.tag_remove("selected_highlight", "1.0", tk.END)
        except Exception as e:
            print(f"清除选中高亮失败: {e}")

    def on_entry_focus_in(self, event):
        """输入框获得焦点时的处理 - 兼容性方法"""
        self.on_combobox_focus_in(event)
    
    def on_entry_focus_out(self, event):
        """输入框失去焦点时的处理 - 兼容性方法"""
        self.on_combobox_focus_out(event)
    
    def on_context_change(self, *args):
        """上下文范围变化时的实时处理 - 保持视图位置"""
        try:
            new_range = int(self.context_var.get())
            if new_range != self.context_range and new_range >= 0:
                self.context_range = new_range
                # 实时更新上下文显示，保持视图位置不跳动
                if self.selected_line_index is not None:
                    self.show_context(self.selected_line_index, preserve_view=True)
        except ValueError:
            pass  # 忽略无效输入

    def on_result_text_click(self, event):
        """处理结果文本点击事件"""
        try:
            # 获取点击位置
            click_pos = self.result_text.index(tk.INSERT)
            line_num = int(click_pos.split('.')[0])
            
            # 计算实际结果索引（减去标题行和分隔符行）
            result_index = line_num - 3  # -1 for title, -1 for separator, -1 for 1-based indexing
            
            print(f"🖱️ 点击行: {line_num}, 计算索引: {result_index}")
            
            if 0 <= result_index < len(self.filtered_results):
                self.selected_line_index = result_index
                self.show_context(result_index)
                
                # 高亮选中的行
                self.highlight_selected_result_line(result_index)
            else:
                print(f"❌ 索引超出范围: {result_index}, 总结果数: {len(self.filtered_results)}")
                
        except Exception as e:
            print(f"结果文本点击处理失败: {e}")

    def highlight_selected_result_line(self, line_index):
        """高亮选中的结果行"""
        try:
            # 清除之前的选中高亮
            self.result_text.tag_remove("selected_result", "1.0", tk.END)
            
            # 计算实际行号（考虑标题行）
            actual_line = line_index + 3  # +1 for title, +1 for separator, +1 for 1-based indexing
            
            # 高亮当前选中的行
            line_start = f"{actual_line}.0"
            line_end = f"{actual_line}.end"
            self.result_text.tag_add("selected_result", line_start, line_end)
            
            # 配置选中行样式
            self.result_text.tag_configure("selected_result", 
                background="#316AC5",  # 蓝色背景
                foreground="#FFFFFF")  # 白色文字
                
        except Exception as e:
            print(f"高亮选中结果行失败: {e}")

    def debug_search_state(self):
        """调试搜索状态"""
        print("🔍 搜索状态调试:")
        print(f"  文件已加载: {'是' if self.file_content else '否'}")
        print(f"  文件行数: {len(self.file_content) if self.file_content else 0}")
        print(f"  当前关键词: '{self.keyword_entry.get()}'")
        print(f"  关键词颜色: {self.keyword_entry.cget('fg')}")
        print(f"  区分大小写: {self.case_var.get()}")
        print(f"  使用正则: {self.regex_var.get()}")
        print(f"  当前结果数: {len(self.filtered_results) if hasattr(self, 'filtered_results') else 0}")
        
        # 显示文件内容预览
        if self.file_content:
            print("  文件内容预览:")
            for i, line in enumerate(self.file_content[:3]):
                print(f"    第{i+1}行: {repr(line[:50])}")
        
        return True
    
    def force_search_refresh(self):
        """强制刷新搜索"""
        try:
            keyword = self.keyword_entry.get().strip()
            if keyword and keyword != "输入关键字，多个关键字用逗号分隔":
                print(f"🔄 强制刷新搜索: {keyword}")
                self.filter_logs()
            else:
                print("⚠️ 无有效关键词可刷新")
        except Exception as e:
            print(f"❌ 强制刷新失败: {e}")

    def load_search_history(self):
        """加载搜索历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                    self.keyword_history = history_data.get('keywords', [])
                    print(f"📚 加载了 {len(self.keyword_history)} 条搜索历史")
            else:
                self.keyword_history = []
                print("📚 未找到历史记录文件，创建新的历史记录")
                
            # 更新下拉列表
            self.update_combobox_values()
            
        except Exception as e:
            print(f"❌ 加载搜索历史失败: {e}")
            self.keyword_history = []
    
    def save_search_history(self):
        """保存搜索历史记录"""
        try:
            history_data = {
                'keywords': self.keyword_history,
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)
                
            print(f"💾 已保存 {len(self.keyword_history)} 条搜索历史")
            
        except Exception as e:
            print(f"❌ 保存搜索历史失败: {e}")
    
    def add_to_search_history(self, keyword):
        """添加关键字到搜索历史"""
        keyword = keyword.strip()
        if not keyword or keyword == "输入关键字，多个关键字用逗号分隔":
            return
        
        try:
            # 如果已存在，先移除
            if keyword in self.keyword_history:
                self.keyword_history.remove(keyword)
            
            # 添加到列表开头
            self.keyword_history.insert(0, keyword)
            
            # 限制历史记录数量（最多保存50条）
            if len(self.keyword_history) > 50:
                self.keyword_history = self.keyword_history[:50]
            
            # 更新下拉列表
            self.update_combobox_values()
            
            # 保存到文件
            self.save_search_history()
            
            print(f"📝 已添加到搜索历史: {keyword}")
            
        except Exception as e:
            print(f"❌ 添加搜索历史失败: {e}")
    
    def update_combobox_values(self):
        """更新下拉框的历史记录选项"""
        try:
            if hasattr(self, 'keyword_combobox'):
                # 保存当前值
                current_value = self.keyword_combobox.get()
                
                # 更新选项列表
                self.keyword_combobox['values'] = self.keyword_history
                
                # 恢复当前值
                self.keyword_combobox.set(current_value)
                
        except Exception as e:
            print(f"❌ 更新下拉框选项失败: {e}")
    
    def clear_search_history(self):
        """清空搜索历史"""
        try:
            result = messagebox.askyesno("确认", "确定要清空所有搜索历史吗？")
            if result:
                self.keyword_history = []
                self.update_combobox_values()
                self.save_search_history()
                messagebox.showinfo("完成", "搜索历史已清空")
                print("🗑️ 已清空搜索历史")
                
        except Exception as e:
            print(f"❌ 清空搜索历史失败: {e}")
    
    def on_combobox_click(self, event):
        """下拉框点击事件处理"""
        # 确保历史记录是最新的
        self.update_combobox_values()
    
    def on_combobox_focus_in(self, event):
        """下拉框获得焦点时的处理"""
        placeholder_text = "输入关键字，多个关键字用逗号分隔"
        if self.keyword_combobox.get() == placeholder_text:
            self.keyword_combobox.set("")
            self.keyword_combobox.config(foreground='black')
    
    def on_combobox_focus_out(self, event):
        """下拉框失去焦点时的处理"""
        if not self.keyword_combobox.get().strip():
            placeholder_text = "输入关键字，多个关键字用逗号分隔"
            self.keyword_combobox.set(placeholder_text)
            self.keyword_combobox.config(foreground='gray')

    def show_history_manager(self):
        """显示历史记录管理窗口"""
        try:
            history_window = tk.Toplevel(self.root)
            history_window.title("📚 搜索历史管理")
            history_window.geometry("600x500")
            history_window.transient(self.root)
            history_window.grab_set()
            
            theme = self.get_current_theme()
            history_window.configure(bg=theme['bg'])
            
            # 标题
            title_frame = tk.Frame(history_window, bg=theme['bg'])
            title_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(title_frame, text="搜索历史记录", font=('Arial', 14, 'bold'),
                    bg=theme['bg'], fg=theme['fg']).pack(side=tk.LEFT)
            
            tk.Label(title_frame, text=f"共 {len(self.keyword_history)} 条记录",
                    bg=theme['bg'], fg=theme['fg']).pack(side=tk.RIGHT)
            
            # 历史记录列表
            list_frame = tk.Frame(history_window, bg=theme['bg'])
            list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            # 创建列表框和滚动条
            listbox_frame = tk.Frame(list_frame, bg=theme['bg'])
            listbox_frame.pack(fill=tk.BOTH, expand=True)
            
            self.history_listbox = tk.Listbox(listbox_frame, height=20)
            scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
            
            self.history_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.history_listbox.yview)
            
            self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 填充历史记录
            for i, keyword in enumerate(self.keyword_history):
                display_text = f"{i+1:2d}. {keyword}"
                self.history_listbox.insert(tk.END, display_text)
            
            # 按钮区域
            button_frame = tk.Frame(history_window, bg=theme['bg'])
            button_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # 使用选中的历史记录
            def use_selected():
                selection = self.history_listbox.curselection()
                if selection:
                    index = selection[0]
                    if index < len(self.keyword_history):
                        selected_keyword = self.keyword_history[index]
                        self.keyword_combobox.set(selected_keyword)
                        self.keyword_combobox.config(foreground='black')
                        history_window.destroy()
                        messagebox.showinfo("提示", f"已选择历史记录: {selected_keyword}")
                else:
                    messagebox.showwarning("提示", "请先选择一个历史记录")
            
            # 删除选中的历史记录
            def delete_selected():
                selection = self.history_listbox.curselection()
                if selection:
                    index = selection[0]
                    if index < len(self.keyword_history):
                        deleted_keyword = self.keyword_history.pop(index)
                        self.history_listbox.delete(index)
                        self.update_combobox_values()
                        self.save_search_history()
                        messagebox.showinfo("完成", f"已删除: {deleted_keyword}")
                        
                        # 更新计数显示
                        for widget in title_frame.winfo_children():
                            if isinstance(widget, tk.Label) and "条记录" in widget.cget("text"):
                                widget.config(text=f"共 {len(self.keyword_history)} 条记录")
                else:
                    messagebox.showwarning("提示", "请先选择一个历史记录")
            
            # 清空所有历史记录
            def clear_all():
                if self.keyword_history:
                    result = messagebox.askyesno("确认", "确定要清空所有搜索历史吗？")
                    if result:
                        self.keyword_history = []
                        self.history_listbox.delete(0, tk.END)
                        self.update_combobox_values()
                        self.save_search_history()
                        messagebox.showinfo("完成", "所有搜索历史已清空")
                        
                        # 更新计数显示
                        for widget in title_frame.winfo_children():
                            if isinstance(widget, tk.Label) and "条记录" in widget.cget("text"):
                                widget.config(text=f"共 {len(self.keyword_history)} 条记录")
                else:
                    messagebox.showinfo("提示", "没有历史记录可清空")
            
            # 按钮
            tk.Button(button_frame, text="✅ 使用选中", command=use_selected,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Button(button_frame, text="🗑️ 删除选中", command=delete_selected,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Button(button_frame, text="🧹 清空全部", command=clear_all,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Button(button_frame, text="❌ 关闭", command=history_window.destroy,
                     bg=theme['button_bg'], fg=theme['button_fg']).pack(side=tk.RIGHT)
            
            # 双击使用历史记录
            def on_double_click(event):
                use_selected()
            
            self.history_listbox.bind('<Double-1>', on_double_click)
            
            # 使用说明
            help_frame = tk.Frame(history_window, bg=theme['bg'])
            help_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            help_text = "💡 提示: 双击历史记录可直接使用，最多保存50条历史记录"
            tk.Label(help_frame, text=help_text, font=('Arial', 9),
                    bg=theme['bg'], fg=theme['fg']).pack()
            
        except Exception as e:
            messagebox.showerror("错误", f"打开历史记录管理失败: {str(e)}")

    def load_bookmarks(self):
        """加载书签"""
        try:
            if os.path.exists(self.bookmarks_file):
                with open(self.bookmarks_file, 'r', encoding='utf-8') as f:
                    bookmark_data = json.load(f)
                    self.bookmarks = bookmark_data.get('bookmarks', [])
                    print(f"🔖 加载了 {len(self.bookmarks)} 个书签")
            else:
                self.bookmarks = []
                print("🔖 未找到书签文件，创建新的书签列表")
                
        except Exception as e:
            print(f"❌ 加载书签失败: {e}")
            self.bookmarks = []
    
    def save_bookmarks(self):
        """保存书签"""
        try:
            bookmark_data = {
                'bookmarks': self.bookmarks,
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
                'version': '1.0'
            }
            
            with open(self.bookmarks_file, 'w', encoding='utf-8') as f:
                json.dump(bookmark_data, f, ensure_ascii=False, indent=2)
                
            print(f"💾 已保存 {len(self.bookmarks)} 个书签")
            
        except Exception as e:
            print(f"❌ 保存书签失败: {e}")
    
    def add_bookmark(self, bookmark):
        """添加书签"""
        try:
            # 检查是否已存在同名书签
            existing_names = [b['name'] for b in self.bookmarks]
            if bookmark['name'] in existing_names:
                result = messagebox.askyesno("书签已存在", 
                                           f"书签 '{bookmark['name']}' 已存在，是否覆盖？")
                if result:
                    # 找到并替换
                    for i, b in enumerate(self.bookmarks):
                        if b['name'] == bookmark['name']:
                            self.bookmarks[i] = bookmark
                            break
                else:
                    return False
            else:
                # 添加新书签
                self.bookmarks.append(bookmark)
            
            # 保存到文件
            self.save_bookmarks()
            print(f"📝 已添加书签: {bookmark['name']}")
            return True
            
        except Exception as e:
            print(f"❌ 添加书签失败: {e}")
            return False
    
    def delete_bookmark(self, bookmark_name):
        """删除书签"""
        try:
            for i, bookmark in enumerate(self.bookmarks):
                if bookmark['name'] == bookmark_name:
                    removed_bookmark = self.bookmarks.pop(i)
                    self.save_bookmarks()
                    print(f"🗑️ 已删除书签: {bookmark_name}")
                    return True
            
            print(f"⚠️ 未找到书签: {bookmark_name}")
            return False
            
        except Exception as e:
            print(f"❌ 删除书签失败: {e}")
            return False
    
    def get_bookmark_by_name(self, name):
        """根据名称获取书签"""
        for bookmark in self.bookmarks:
            if bookmark['name'] == name:
                return bookmark
        return None
    
    def apply_bookmark(self, bookmark):
        """应用书签设置"""
        try:
            # 设置搜索关键字
            self.keyword_combobox.set(bookmark['keywords'])
            self.keyword_combobox.config(foreground='black')
            
            # 设置搜索选项
            self.case_var.set(bookmark.get('case_sensitive', False))
            self.regex_var.set(bookmark.get('use_regex', False))
            self.logic_var.set(bookmark.get('search_logic', 'OR'))
            
            # 设置上下文范围
            context_range = bookmark.get('context_range', 2)
            self.context_var.set(str(context_range))
            self.context_range = context_range
            
            print(f"✅ 已应用书签: {bookmark['name']}")
            return True
            
        except Exception as e:
            print(f"❌ 应用书签失败: {e}")
            return False

    def on_result_text_right_click(self, event):
        """处理搜索结果右键菜单"""
        try:
            # 创建右键菜单
            context_menu = tk.Menu(self.root, tearoff=0)
            
            # 快速添加书签
            def quick_add_bookmark():
                current_search = self.keyword_entry.get().strip()
                placeholder_text = "输入关键字，多个关键字用逗号分隔"
                
                if not current_search or current_search == placeholder_text:
                    messagebox.showwarning("警告", "没有当前搜索内容可保存")
                    return
                
                # 简单对话框获取书签名称
                bookmark_name = simpledialog.askstring("添加书签", "请输入书签名称:", 
                                                       initialvalue=f"搜索_{current_search[:20]}")
                
                if bookmark_name:
                    bookmark = {
                        'name': bookmark_name,
                        'keywords': current_search,
                        'case_sensitive': self.case_var.get(),
                        'use_regex': self.regex_var.get(),
                        'search_logic': self.logic_var.get(),
                        'context_range': self.context_range,
                        'created_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'file_info': os.path.basename(getattr(self, 'current_file_path', '未知文件'))
                    }
                    
                    if self.add_bookmark(bookmark):
                        messagebox.showinfo("成功", f"书签 '{bookmark_name}' 已添加")
            
            # 添加菜单项
            context_menu.add_command(label="📝 快速添加书签", command=quick_add_bookmark)
            context_menu.add_separator()
            context_menu.add_command(label="🔖 管理书签", command=self.show_bookmarks)
            
            # 显示菜单
            context_menu.post(event.x_root, event.y_root)
            
        except Exception as e:
            print(f"右键菜单处理失败: {e}")

def main():
    """主函数"""
    print("🚀 启动超级现代化日志分析工具...")
    
    try:
        app = LogFilterApp()
        
        # 检查UI增强器状态
        if hasattr(app, 'ui_enhancer'):
            print("✨ UI增强器已成功应用!")
            print(f"📱 当前主题: {app.current_theme}")
            print(f"🎨 可用主题: {list(app.themes.keys())}")
        
        print("🎉 应用启动成功!")
        app.root.mainloop()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
