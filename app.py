"""
产品简章折页设计工具 v1.0
支持二折页、三折页、四折页的设计和导出
作者：微酱
"""

import streamlit as st
import os
import json
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="产品简章折页设计工具",
    page_icon="📄",
    layout="wide"
)

st.title("📄 产品简章折页设计工具")
st.markdown("---")

# 加载模版配置
def load_templates():
    config_path = os.path.join(os.path.dirname(__file__), "templates", "templates.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 侧边栏 - 项目设置
with st.sidebar:
    st.header("📋 项目设置")
    
    # 折页类型
    fold_type = st.selectbox(
        "折页类型",
        options=["三折页", "四折页", "二折页"],
        index=0
    )
    
    # 尺寸显示
    size_map = {
        "二折页": "360mm × 285mm",
        "三折页": "540mm × 285mm", 
        "四折页": "720mm × 285mm"
    }
    st.info(f"📐 尺寸：{size_map[fold_type]}")
    
    # 设计风格
    templates = load_templates()
    if templates:
        style_options = list(templates.get("styles", {}).keys())
    else:
        style_options = ["橙色科技风", "红色商务风", "蓝色商务风", "绿色清新风"]
    
    style = st.selectbox("设计风格", options=style_options)
    
    st.markdown("---")
    st.markdown("### 📖 使用说明")
    st.markdown("""
    1. 选择折页类型和风格
    2. 依次填写各面内容
    3. 上传需要的图片
    4. 预览并导出PDF
    """)

# 主内容区
tabs = st.tabs(["封面", "痛点页", "解决方案", "课程安排", "讲师介绍", "学习指南"])

# 封面设置
with tabs[0]:
    st.header("🎨 封面设计")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("产品名称", placeholder="如：AI销售训战")
        product_slogan = st.text_input("Slogan", placeholder="如：像复制文件一样复制销冠")
        
        # 核心卖点
        st.subheader("核心卖点（3-5条）")
        selling_points = []
        for i in range(5):
            point = st.text_input(f"卖点 {i+1}", key=f"sp_{i}", placeholder=f"输入第{i+1}条卖点")
            if point:
                selling_points.append(point)
        
        version = st.text_input("版本号", placeholder="如：L06-2603-V01")
    
    with col2:
        # 封面图片
        st.subheader("封面图片")
        cover_image = st.file_uploader("上传封面主图", type=['png', 'jpg', 'jpeg'])
        if cover_image:
            st.image(cover_image, width=300)

# 痛点页
with tabs[1]:
    st.header("😰 痛点设计")
    
    pain_title = st.text_input("痛点标题", value="您的企业是否有以下问题？")
    
    st.subheader("痛点列表（4-6条）")
    pain_points = []
    for i in range(6):
        col1, col2 = st.columns([3, 1])
        with col1:
            point = st.text_area(
                f"痛点 {i+1}", 
                key=f"pain_{i}", 
                height=80,
                placeholder=f"输入第{i+1}条痛点描述"
            )
        with col2:
            icon = st.selectbox(
                "图标", 
                options=["❓", "⚠️", "❌", "💡", "🎯", "📊"],
                key=f"pain_icon_{i}"
            )
        if point:
            pain_points.append({"text": point, "icon": icon})

# 解决方案
with tabs[2]:
    st.header("💡 解决方案")
    
    solution_title = st.text_input("解决方案标题", value="突围之道")
    solution_intro = st.text_area("方案简介", height=100, placeholder="简要介绍解决方案的核心价值")
    
    st.subheader("功能模块（3-6个）")
    modules = []
    for i in range(6):
        col1, col2 = st.columns([1, 3])
        with col1:
            module_name = st.text_input(f"模块{i+1}名称", key=f"module_name_{i}")
        with col2:
            module_desc = st.text_area(f"模块{i+1}描述", key=f"module_desc_{i}", height=60)
        if module_name:
            modules.append({"name": module_name, "desc": module_desc})

# 课程安排
with tabs[3]:
    st.header("📅 课程安排")
    
    has_schedule = st.checkbox("包含课程安排表", value=True)
    
    if has_schedule:
        schedule_title = st.text_input("表格标题", value="课程安排")
        
        # 课程时间
        course_duration = st.text_input("课程时长", placeholder="如：2天1晚")
        course_location = st.text_input("授课地点", placeholder="如：深圳")
        
        st.subheader("课程模块")
        course_modules = []
        for i in range(8):
            col1, col2 = st.columns([1, 3])
            with col1:
                module_time = st.text_input(f"时间/Day", key=f"course_time_{i}")
            with col2:
                module_content = st.text_input(f"内容", key=f"course_content_{i}")
            if module_content:
                course_modules.append({"time": module_time, "content": module_content})

# 讲师介绍
with tabs[4]:
    st.header("👨‍🏫 讲师介绍")
    
    has_teacher = st.checkbox("包含讲师介绍", value=True)
    
    if has_teacher:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            teacher_photo = st.file_uploader("讲师照片", type=['png', 'jpg', 'jpeg'])
            if teacher_photo:
                st.image(teacher_photo, width=200)
        
        with col2:
            teacher_name = st.text_input("讲师姓名", placeholder="如：董仁杰")
            teacher_title = st.text_input("讲师头衔", placeholder="如：原中兴通讯海外子公司总经理")
            
            st.subheader("讲师经历")
            teacher_experiences = []
            for i in range(6):
                exp = st.text_input(f"经历 {i+1}", key=f"teacher_exp_{i}")
                if exp:
                    teacher_experiences.append(exp)

# 学习指南
with tabs[5]:
    st.header("📖 学习指南")
    
    guide_items = {
        "适合对象": st.text_input("适合对象", placeholder="如：企业老板、销售负责人"),
        "学习时间": st.text_input("学习时间", placeholder="如：3天2晚"),
        "收费标准": st.text_input("收费标准", placeholder="如：2.98万/人"),
        "报名方式": st.text_input("报名方式", placeholder="如：联系学习顾问报名")
    }
    
    st.subheader("二维码")
    col1, col2 = st.columns(2)
    with col1:
        qr_code1 = st.file_uploader("二维码1（产品介绍/报名）", type=['png', 'jpg', 'jpeg'])
        if qr_code1:
            st.image(qr_code1, width=150)
    with col2:
        qr_code2 = st.file_uploader("二维码2（可选）", type=['png', 'jpg', 'jpeg'])
        if qr_code2:
            st.image(qr_code2, width=150)

# 底部操作区
st.markdown("---")
st.header("📤 导出")

col1, col2, col3 = st.columns(3)

with col1:
    project_name = st.text_input("项目名称", value="产品简章")

with col2:
    if st.button("👁️ 预览效果", type="secondary"):
        st.info("预览功能开发中...")

with col3:
    if st.button("📥 导出PDF", type="primary"):
        # 收集所有数据
        project_data = {
            "fold_type": fold_type,
            "style": style,
            "product_name": product_name,
            "product_slogan": product_slogan,
            "selling_points": selling_points,
            "version": version,
            "pain_title": pain_title,
            "pain_points": pain_points,
            "solution_title": solution_title,
            "solution_intro": solution_intro,
            "modules": modules,
            "course_modules": course_modules if has_schedule else [],
            "course_duration": course_duration if has_schedule else "",
            "course_location": course_location if has_schedule else "",
            "teacher_name": teacher_name if has_teacher else "",
            "teacher_title": teacher_title if has_teacher else "",
            "teacher_experiences": teacher_experiences if has_teacher else [],
            "guide_items": guide_items
        }
        
        # 保存项目数据
        data_path = f"折页设计工具/projects/{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        
        st.success(f"✅ 项目数据已保存")
        st.info("PDF生成功能开发中，敬请期待...")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px;">
    Made with ❤️ by 微酱 | v1.0 折页设计工具
</div>
""", unsafe_allow_html=True)
