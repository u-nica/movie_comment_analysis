import tkinter as tk
from tkinter import messagebox
import movies
import movies_analysis
import comments
import comment_analysis

def run_movies():
    movies.run()
    messagebox.showinfo("提示", "电影数据爬取完成！")

def run_movies_analysis():
    movies_analysis.run()
    messagebox.showinfo("提示", "电影数据分析完成！")

def run_comments():
    comments.run()
    messagebox.showinfo("提示", "评论数据爬取完成！")

def run_comment_analysis():
    comment_analysis.run()
    messagebox.showinfo("提示", "评论数据分析完成！")

def create_gui():
    # 创建主窗口
    root = tk.Tk()
    root.title("豆瓣高分电影数据管理")
    root.geometry("300x300")  # 设置窗口大小

    # 创建按钮
    btn_movies = tk.Button(root, text="爬取豆瓣高分电影数据", command=run_movies)
    btn_movies.pack(pady=10)

    btn_movies_analysis = tk.Button(root, text="分析豆瓣高分电影数据", command=run_movies_analysis)
    btn_movies_analysis.pack(pady=10)

    btn_comments = tk.Button(root, text="爬取指定电影评论", command=run_comments)
    btn_comments.pack(pady=10)

    btn_comment_analysis = tk.Button(root, text="分析指定电影评论数据", command=run_comment_analysis)
    btn_comment_analysis.pack(pady=10)

    # 启动GUI主循环
    root.mainloop()

if __name__ == "__main__":
    create_gui()
