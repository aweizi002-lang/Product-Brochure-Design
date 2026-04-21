"""
产品简章折页设计工具 v2.5
日系简约UI设计 + Pollinations.AI高清文生图
作者：微酱
"""

import streamlit as st
import os
import json
from datetime import datetime
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

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

def call_image_api(prompt, config=None, size="1536x1024"):
    """使用Pollinations.AI免费生成图片（无需API Key）"""
    try:
        # 解析尺寸
        width, height = size.split("x")
        
        # 构建Pollinations.AI URL - 高清版本
        encoded_prompt = requests.utils.quote(prompt)
        # 使用flux模型，增加enhance参数提升质量
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&enhance=true&nologo=true"
        
        # 测试URL是否可访问
        response = requests.head(image_url, timeout=10)
        if response.status_code == 200:
            return image_url, "成功"
        
        # 如果HEAD失败，直接返回URL（图片会在加载时生成）
        return image_url, "成功"
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
    st.markdown("### 🎨 AI生图")
    st.info("✨ 免费使用，无需配置")

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
                with st.spinner("生成中..."):
                    image_url, msg = call_image_api(prompt_text)
                if image_url:
                    st.success("✅ 生成成功")
                    st.session_state["generated_images"]["cover"] = image_url
                else:
                    st.error(msg)
        
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
                with st.spinner("生成中..."):
                    img_url, msg = call_image_api(pain_prompt)
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
                    with st.spinner("生成中..."):
                        img_url, msg = call_image_api(t_prompt)
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

# 预览功能
if "show_preview" not in st.session_state:
    st.session_state["show_preview"] = False

with col2:
    if st.button("预览效果"):
        st.session_state["show_preview"] = True

with col3:
    if st.button("导出PDF", type="primary"):
        st.session_state["show_preview"] = True
        st.session_state["export_pdf"] = True

# ==================== 预览渲染 ====================
def generate_preview_html(fold_type, style, product_name, slogan, cover_image, 
                          selling_points, pain_points, solution_title, solution_intro, 
                          modules, course_modules, course_duration, course_location,
                          teacher_name, teacher_title, teacher_experiences, teacher_image,
                          guide, qr_images):
    """生成折页预览HTML"""
    
    # 风格颜色映射
    style_colors = {
        "橙色科技风": {"primary": "#ff6b35", "secondary": "#f7931e", "bg": "#fff8f0"},
        "红色商务风": {"primary": "#c41e3a", "secondary": "#8b0000", "bg": "#fff5f5"},
        "蓝色商务风": {"primary": "#1e88e5", "secondary": "#0d47a1", "bg": "#f0f7ff"},
        "绿色清新风": {"primary": "#43a047", "secondary": "#2e7d32", "bg": "#f0fff0"},
        "紫色高端风": {"primary": "#7b1fa2", "secondary": "#4a148c", "bg": "#faf0ff"},
        "金色尊贵风": {"primary": "#d4a574", "secondary": "#b8860b", "bg": "#fffaf0"}
    }
    colors = style_colors.get(style, style_colors["橙色科技风"])
    
    # 页面数量
    pages = {"二折页": 4, "三折页": 6, "四折页": 8}
    page_count = pages.get(fold_type, 6)
    
    html = f"""
    <style>
        .brochure-preview {{
            width: 100%;
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .preview-pages {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        }}
        .preview-page {{
            width: 180px;
            height: 142px;
            background: white;
            border: 2px solid {colors['primary']};
            border-radius: 4px;
            padding: 10px;
            font-size: 10px;
            overflow: hidden;
            position: relative;
        }}
        .preview-page .page-label {{
            position: absolute;
            top: 5px;
            right: 5px;
            background: {colors['primary']};
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 9px;
        }}
        .preview-page h3 {{
            color: {colors['primary']};
            font-size: 12px;
            margin: 15px 0 8px 0;
            border-bottom: 1px solid {colors['primary']};
            padding-bottom: 4px;
        }}
        .preview-page p {{
            color: #333;
            font-size: 9px;
            margin: 3px 0;
            line-height: 1.3;
        }}
        .preview-cover {{
            background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
        .preview-cover h2 {{
            color: white;
            font-size: 14px;
            margin: 5px 0;
        }}
        .preview-cover .slogan {{
            font-size: 9px;
            opacity: 0.9;
        }}
        .preview-item {{
            display: flex;
            align-items: flex-start;
            margin: 4px 0;
        }}
        .preview-item .icon {{
            margin-right: 5px;
        }}
        .preview-note {{
            text-align: center;
            color: #888;
            font-size: 12px;
            margin-top: 15px;
        }}
    </style>
    <div class="brochure-preview">
        <div style="text-align:center; color:{colors['primary']}; font-weight:500; margin-bottom:15px;">
            📄 {fold_type}预览（{page_count}面）- {style}
        </div>
        <div class="preview-pages">
    """
    
    # 封面
    html += f"""
        <div class="preview-page preview-cover">
            <span class="page-label">封面</span>
            <h2>{product_name or '产品名称'}</h2>
            <p class="slogan">{slogan or '产品Slogan'}</p>
        </div>
    """
    
    # 痛点页
    pain_html = "".join([f'<div class="preview-item"><span class="icon">{p["icon"]}</span><span>{p["text"]}</span></div>' for p in pain_points[:4]]) if pain_points else '<p>点击"痛点"标签填写</p>'
    html += f"""
        <div class="preview-page">
            <span class="page-label">痛点</span>
            <h3>核心痛点</h3>
            {pain_html}
        </div>
    """
    
    # 方案页
    modules_html = "".join([f'<p>▸ {m["name"]}</p>' for m in modules[:4]]) if modules else '<p>点击"方案"标签填写</p>'
    html += f"""
        <div class="preview-page">
            <span class="page-label">方案</span>
            <h3>{solution_title or '解决方案'}</h3>
            <p>{solution_intro[:50] + '...' if solution_intro and len(solution_intro) > 50 else solution_intro or ''}</p>
            {modules_html}
        </div>
    """
    
    # 课程页
    if course_modules:
        course_html = "".join([f'<p>{c["time"]} {c["content"]}</p>' for c in course_modules[:4]])
        html += f"""
        <div class="preview-page">
            <span class="page-label">课程</span>
            <h3>课程安排</h3>
            <p>📍 {course_location or '地点'} | ⏰ {course_duration or '时长'}</p>
            {course_html}
        </div>
        """
    
    # 讲师页
    if teacher_name:
        exp_html = "".join([f'<p>• {e}</p>' for e in teacher_experiences[:3]])
        html += f"""
        <div class="preview-page">
            <span class="page-label">讲师</span>
            <h3>讲师介绍</h3>
            <p><strong>{teacher_name}</strong></p>
            <p style="color:{colors['primary']}">{teacher_title}</p>
            {exp_html}
        </div>
        """
    
    # 指南页
    guide_html = "".join([f'<p><strong>{k}:</strong> {v}</p>' for k, v in list(guide.items())[:4] if v])
    if guide_html:
        html += f"""
        <div class="preview-page">
            <span class="page-label">指南</span>
            <h3>学习指南</h3>
            {guide_html}
        </div>
        """
    
    # 封底
    html += f"""
        <div class="preview-page preview-cover">
            <span class="page-label">封底</span>
            <h2>扫码咨询</h2>
            <p class="slogan">期待您的加入</p>
        </div>
    """
    
    html += """
        </div>
        <p class="preview-note">💡 提示：这是简化预览，实际折页会根据排版优化布局</p>
    </div>
    """
    
    return html

# 显示预览
if st.session_state.get("show_preview"):
    st.markdown("---")
    
    # 获取所有数据 - 使用安全的变量获取方式
    cover_img = st.session_state.get("generated_images", {}).get("cover", "")
    teacher_img = st.session_state.get("generated_images", {}).get("teacher", "")
    
    # 安全获取变量（避免未定义错误）
    try:
        sp = selling_points
    except NameError:
        sp = []
    
    try:
        pp = pain_points
    except NameError:
        pp = []
    
    try:
        stitle = solution_title
    except NameError:
        stitle = ""
    
    try:
        sintro = solution_intro
    except NameError:
        sintro = ""
    
    try:
        mods = modules
    except NameError:
        mods = []
    
    try:
        cm = course_modules
    except NameError:
        cm = []
    
    try:
        cd = course_duration
    except NameError:
        cd = ""
    
    try:
        cl = course_location
    except NameError:
        cl = ""
    
    try:
        tname = teacher_name
    except NameError:
        tname = ""
    
    try:
        ttitle = teacher_title
    except NameError:
        ttitle = ""
    
    try:
        texps = teacher_experiences
    except NameError:
        texps = []
    
    try:
        g = guide
    except NameError:
        g = {}
    
    preview_html = generate_preview_html(
        fold_type=fold_type,
        style=style,
        product_name=product_name,
        slogan=product_slogan,
        cover_image=cover_img,
        selling_points=sp,
        pain_points=pp,
        solution_title=stitle,
        solution_intro=sintro,
        modules=mods,
        course_modules=cm,
        course_duration=cd,
        course_location=cl,
        teacher_name=tname,
        teacher_title=ttitle,
        teacher_experiences=texps,
        teacher_image=teacher_img,
        guide=g,
        qr_images=[]
    )
    
    st.markdown(preview_html, unsafe_allow_html=True)
    
    # 关闭预览按钮
    if st.button("关闭预览"):
        st.session_state["show_preview"] = False
        st.rerun()

# 页脚
st.markdown("""
<div class="footer">
    Made with 🌸 by 微酱 | v2.5 高清生图版
</div>
""", unsafe_allow_html=True)
