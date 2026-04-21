"""
产品简章折页设计工具 v2.2
日系简约UI设计 + 在线AI文生图（Kolors免费模型）
作者：微酱
"""

import streamlit as st
import os
import json
from datetime import datetime
import requests
from io import BytesIO
from PIL import Image

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="产品简章折页设计工具",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 日系UI CSS ====================
st.markdown("""
<style>
    /* 导入日系字体 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    /* 主背景 - 温暖米白色 */
    .stApp {
        background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
        font-family: 'Noto Sans SC', 'Hiragino Sans GB', sans-serif;
    }
    
    /* 隐藏默认标题 */
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    /* 主标题 */
    .main-title {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    
    .main-title h1 {
        color: #4a4a4a;
        font-size: 28px;
        font-weight: 300;
        letter-spacing: 8px;
        margin: 0;
    }
    
    .main-title .subtitle {
        color: #9a9a9a;
        font-size: 13px;
        letter-spacing: 4px;
        margin-top: 10px;
    }
    
    /* 装饰线 */
    .deco-line {
        width: 60px;
        height: 1px;
        background: #d4a574;
        margin: 20px auto;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #eee;
        box-shadow: 2px 0 10px rgba(0,0,0,0.02);
    }
    
    [data-testid="stSidebar"] h3 {
        color: #5a5a5a;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 2px;
        padding-bottom: 10px;
        border-bottom: 1px solid #eee;
    }
    
    /* 标签 */
    h2, h3, h4 {
        color: #5a5a5a;
        font-weight: 400;
        letter-spacing: 1px;
    }
    
    /* 输入框 */
    .stTextInput input, .stTextArea textarea {
        background: #ffffff;
        border: 1px solid #e8e8e8;
        border-radius: 4px;
        color: #4a4a4a;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #d4a574;
        box-shadow: 0 0 0 3px rgba(212, 165, 116, 0.1);
    }
    
    .stTextInput input::placeholder {
        color: #bbb;
    }
    
    /* 下拉框 */
    .stSelectbox div[data-baseweb="select"] {
        background: #fff;
        border: 1px solid #e8e8e8;
        border-radius: 4px;
    }
    
    /* 按钮 */
    .stButton button {
        background: #d4a574;
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 400;
        letter-spacing: 2px;
        padding: 12px 32px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(212, 165, 116, 0.2);
    }
    
    .stButton button:hover {
        background: #c49564;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(212, 165, 116, 0.3);
    }
    
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* 主按钮 */
    .stButton button[kind="primary"] {
        background: #7eb5a6;
    }
    
    .stButton button[kind="primary"]:hover {
        background: #6ea596;
    }
    
    /* Tab标签 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #eee;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #9a9a9a;
        font-size: 13px;
        font-weight: 400;
        letter-spacing: 1px;
        padding: 15px 25px;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #d4a574;
    }
    
    .stTabs [aria-selected="true"] {
        color: #d4a574;
        border-bottom-color: #d4a574;
        background: transparent;
    }
    
    /* 信息提示 */
    .stSuccess {
        background: #f0f9f6;
        border: 1px solid #c8e6dc;
        color: #5a8a7a;
    }
    
    .stInfo {
        background: #faf5f0;
        border: 1px solid #e8ddd0;
        color: #8a7a6a;
    }
    
    .stWarning {
        background: #fff9f0;
        border: 1px solid #f0e0c8;
        color: #9a7a5a;
    }
    
    /* 卡片 */
    .card {
        background: #fff;
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #f0f0f0;
    }
    
    /* 上传区域 */
    [data-testid="stFileUploader"] {
        background: #fafafa;
        border: 2px dashed #e0e0e0;
        border-radius: 8px;
        padding: 25px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #d4a574;
        background: #faf5f0;
    }
    
    /* 复选框 */
    .stCheckbox label {
        color: #6a6a6a;
    }
    
    /* 分割线 */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e8e8e8, transparent);
        margin: 30px 0;
    }
    
    /* 代码块 */
    .stCode, code {
        background: #f8f6f4;
        border: 1px solid #eee;
        border-radius: 4px;
        color: #6a6a6a;
    }
    
    /* 滚动条 */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f5f5f5;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #ddd;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #ccc;
    }
    
    /* 页脚 */
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 12px;
        padding: 40px 0;
        letter-spacing: 2px;
    }
    
    /* 标签样式 */
    .tag {
        display: inline-block;
        background: #f5f0e8;
        color: #8a7a6a;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        margin: 0 4px;
    }
    
    /* 装饰元素 */
    .sakura {
        color: #f0c0c0;
        font-size: 14px;
    }
    
    /* 加载 */
    .stSpinner > div {
        border-color: #d4a574 transparent transparent transparent;
    }
    
    /* 隐藏streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== 标题区 ====================
st.markdown("""
<div class="main-title">
    <h1>折页设计工具</h1>
    <div class="deco-line"></div>
    <div class="subtitle">Brochure Design Studio</div>
</div>
""", unsafe_allow_html=True)

# ==================== API配置 ====================
def get_api_config():
    api_key = os.environ.get("SILICONFLOW_API_KEY", "")
    if api_key:
        return {
            "api_key": api_key,
            "api_url": "https://api.siliconflow.cn/v1/images/generations",
            "model": "stabilityai/stable-diffusion-3-medium"
        }
    
    config_path = os.path.join(os.path.dirname(__file__), "api_config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# ==================== 关键词映射 ====================
SCENE_KEYWORDS = {
    "销售": ["销售团队", "商务谈判", "业绩增长", "签单成交"],
    "财务": ["财务报表", "数据分析", "资金流", "企业决策"],
    "AI": ["人工智能", "智能系统", "数据可视化", "科技感"],
    "管理": ["团队管理", "领导力", "战略规划"],
    "总裁": ["高层决策", "战略视野", "商业领袖"]
}

STYLE_PROMPTS = {
    "橙色科技风": "科技感，橙色渐变，现代商务，数据可视化",
    "红色商务风": "商务专业，红色主调，稳重高端，企业级",
    "蓝色商务风": "商务科技，蓝色渐变，专业可信，智能化",
    "绿色清新风": "清新自然，绿色主调，活力成长，健康向上",
    "紫色高端风": "高端奢华，紫色渐变，尊贵典雅，精英气质",
    "金色尊贵风": "金色质感，尊贵大气，高端商务，成功氛围"
}

# ==================== 工具函数 ====================
def generate_image_prompt(title, style, scene_type="封面"):
    detected_scenes = []
    for keyword, scenes in SCENE_KEYWORDS.items():
        if keyword in title:
            detected_scenes.extend(scenes[:2])
    
    style_desc = STYLE_PROMPTS.get(style, "现代商务风格")
    
    if detected_scenes:
        scene_desc = "、".join(detected_scenes[:3])
        prompt = f"{title}主题，{scene_desc}，{style_desc}"
    else:
        prompt = f"{title}产品宣传，{style_desc}"
    
    if scene_type == "封面":
        prompt += "，产品宣传封面，高质量商业设计，4k"
    else:
        prompt += "，信息配图，简洁清晰"
    
    return prompt

def call_image_api(prompt, config, size="1024x1024"):
    if not config or not config.get("api_key"):
        return None, "请先配置API Key"
    
    try:
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": config.get("model", "Kwai-Kolors/Kolors"),
            "prompt": prompt,
            "image_size": size,
            "num_images": 1
        }
        
        response = requests.post(config["api_url"], headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "images" in result and len(result["images"]) > 0:
                return result["images"][0].get("url"), "成功"
        return None, f"API错误: {response.status_code}"
    except Exception as e:
        return None, f"生成失败: {str(e)}"

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("### ⚙️ 设置")
    
    st.markdown("#### 折页类型")
    fold_type = st.selectbox("", ["三折页", "四折页", "二折页"], label_visibility="collapsed")
    
    size_map = {"二折页": "360 × 285 mm", "三折页": "540 × 285 mm", "四折页": "720 × 285 mm"}
    st.info(f"📐 {size_map[fold_type]}")
    
    st.markdown("#### 设计风格")
    style = st.selectbox("", list(STYLE_PROMPTS.keys()), label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 🔑 API配置")
    
    api_config = get_api_config()
    if api_config and api_config.get("api_key"):
        st.success("✅ API已配置")
    else:
        st.warning("⚠️ 请配置API Key")
        api_key_input = st.text_input("API Key", type="password", label_visibility="collapsed")
        if api_key_input:
            st.session_state["api_key"] = api_key_input
            st.success("已保存")

def get_current_api_config():
    config = get_api_config()
    if not config and "api_key" in st.session_state:
        return {"api_key": st.session_state["api_key"], 
                "api_url": "https://api.siliconflow.cn/v1/images/generations",
                "model": "stabilityai/stable-diffusion-3-medium"}
    return config

# ==================== 主内容 ====================
tab_names = ["封面", "痛点", "方案", "课程", "讲师", "指南"]
tab_icons = ["🎨", "💭", "💡", "📅", "👤", "📋"]
tabs = st.tabs([f"{tab_icons[i]} {name}" for i, name in enumerate(tab_names)])

if "generated_images" not in st.session_state:
    st.session_state["generated_images"] = {}

# ==================== 封面 ====================
with tabs[0]:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 基本信息")
        product_name = st.text_input("产品名称", placeholder="如：销售训战")
        product_slogan = st.text_input("Slogan", placeholder="如：像复制文件一样复制销冠")
        
        st.markdown("#### AI封面图")
        
        if product_name:
            auto_prompt = generate_image_prompt(product_name, style, "封面")
            prompt_text = st.text_area("提示词", value=auto_prompt, height=70)
            
            if st.button("生成封面图", type="primary"):
                current_config = get_current_api_config()
                if current_config:
                    with st.spinner("生成中..."):
                        image_url, msg = call_image_api(prompt_text, current_config)
                    if image_url:
                        st.success("✅ 生成成功")
                        st.session_state["generated_images"]["cover"] = image_url
                    else:
                        st.error(msg)
                else:
                    st.error("请先配置API Key")
        
        if "cover" in st.session_state.get("generated_images", {}):
            st.image(st.session_state["generated_images"]["cover"], use_column_width=True)
        
        st.markdown("#### 核心卖点")
        selling_points = []
        c1, c2 = st.columns(2)
        for i in range(4):
            with c1 if i < 2 else c2:
                point = st.text_input(f"卖点 {i+1}", key=f"sp_{i}")
                if point:
                    selling_points.append(point)
        
        version = st.text_input("版本号", placeholder="L06-2603-V01")
    
    with col2:
        st.markdown("#### 上传图片")
        cover_upload = st.file_uploader("或上传已有封面图", type=['png', 'jpg', 'jpeg'])
        if cover_upload:
            st.image(cover_upload, use_column_width=True)

# ==================== 痛点 ====================
with tabs[1]:
    pain_title = st.text_input("痛点标题", value="您的企业是否有以下问题？")
    
    col1, col2 = st.columns(2)
    with col1:
        if product_name:
            pain_prompt = generate_image_prompt(product_name + "困境", style, "配图")
            st.text_area("配图提示词", value=pain_prompt, height=50, key="pain_prompt")
            if st.button("生成痛点配图"):
                current_config = get_current_api_config()
                if current_config:
                    with st.spinner("生成中..."):
                        img_url, msg = call_image_api(pain_prompt, current_config)
                    if img_url:
                        st.session_state["generated_images"]["pain"] = img_url
    
    with col2:
        if "pain" in st.session_state.get("generated_images", {}):
            st.image(st.session_state["generated_images"]["pain"], width=280)
    
    st.markdown("#### 痛点列表")
    pain_points = []
    for i in range(6):
        c1, c2 = st.columns([1, 5])
        with c1:
            icon = st.selectbox("", ["❓", "⚠️", "❌", "💡", "🎯"], key=f"icon_{i}", label_visibility="collapsed")
        with c2:
            text = st.text_input(f"痛点 {i+1}", key=f"pain_{i}", label_visibility="collapsed")
        if text:
            pain_points.append({"icon": icon, "text": text})

# ==================== 方案 ====================
with tabs[2]:
    solution_title = st.text_input("方案标题", value="突围之道")
    solution_intro = st.text_area("方案简介", height=70)
    
    st.markdown("#### 功能模块")
    modules = []
    for i in range(6):
        c1, c2 = st.columns([1, 3])
        with c1:
            name = st.text_input(f"模块 {i+1}", key=f"mod_{i}", label_visibility="collapsed")
        with c2:
            desc = st.text_area("描述", key=f"mod_desc_{i}", height=50, label_visibility="collapsed")
        if name:
            modules.append({"name": name, "desc": desc})

# ==================== 课程 ====================
with tabs[3]:
    has_schedule = st.checkbox("包含课程安排", value=True)
    course_modules = []
    course_duration = ""
    course_location = ""
    
    if has_schedule:
        c1, c2 = st.columns(2)
        with c1:
            course_duration = st.text_input("课程时长", placeholder="2天1晚")
        with c2:
            course_location = st.text_input("授课地点", placeholder="深圳")
        
        st.markdown("#### 课程模块")
        for i in range(6):
            c1, c2 = st.columns([1, 3])
            with c1:
                time = st.text_input("时间", key=f"time_{i}", label_visibility="collapsed")
            with c2:
                content = st.text_input("内容", key=f"content_{i}", label_visibility="collapsed")
            if content:
                course_modules.append({"time": time, "content": content})

# ==================== 讲师 ====================
with tabs[4]:
    has_teacher = st.checkbox("包含讲师介绍", value=True)
    teacher_name = ""
    teacher_title = ""
    teacher_experiences = []
    
    if has_teacher:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("#### 讲师照片")
            teacher_desc = st.text_input("形象描述", placeholder="中年男性，商务西装")
            if teacher_desc:
                t_prompt = f"{teacher_desc}，职业商务肖像照"
                if st.button("生成讲师照"):
                    current_config = get_current_api_config()
                    if current_config:
                        with st.spinner("生成中..."):
                            img_url, msg = call_image_api(t_prompt, current_config)
                        if img_url:
                            st.session_state["generated_images"]["teacher"] = img_url
            
            if "teacher" in st.session_state.get("generated_images", {}):
                st.image(st.session_state["generated_images"]["teacher"], width=180)
            
            teacher_upload = st.file_uploader("或上传照片", type=['png', 'jpg', 'jpeg'])
            if teacher_upload:
                st.image(teacher_upload, width=180)
        
        with c2:
            teacher_name = st.text_input("讲师姓名", placeholder="董仁杰")
            teacher_title = st.text_input("讲师头衔", placeholder="原中兴通讯海外子公司总经理")
            
            st.markdown("#### 讲师经历")
            for i in range(4):
                exp = st.text_input(f"经历 {i+1}", key=f"exp_{i}")
                if exp:
                    teacher_experiences.append(exp)

# ==================== 指南 ====================
with tabs[5]:
    st.markdown("#### 学习指南")
    guide = {}
    for label in ["适合对象", "学习时间", "收费标准", "报名方式"]:
        guide[label] = st.text_input(label, placeholder=f"输入{label}")
    
    st.markdown("#### 二维码")
    c1, c2 = st.columns(2)
    with c1:
        qr1 = st.file_uploader("二维码 1", type=['png', 'jpg'])
        if qr1:
            st.image(qr1, width=140)
    with c2:
        qr2 = st.file_uploader("二维码 2", type=['png', 'jpg'])
        if qr2:
            st.image(qr2, width=140)

# ==================== 导出 ====================
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    project_name = st.text_input("项目名称", value=product_name or "产品简章")

with col2:
    if st.button("预览效果"):
        st.info("预览功能开发中...")

with col3:
    if st.button("导出PDF", type="primary"):
        st.success("PDF导出功能开发中...")

# 页脚
st.markdown("""
<div class="footer">
    Made with 🌸 by 微酱 | v2.1 日系简约版
</div>
""", unsafe_allow_html=True)
