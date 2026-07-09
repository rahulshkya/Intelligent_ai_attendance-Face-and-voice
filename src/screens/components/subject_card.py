import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):

    st.markdown("""
<style>

.subject-card{
    position:relative;
    overflow:hidden;

    background:rgba(18,24,38,.82);
    backdrop-filter:blur(18px);

    border:1px solid rgba(255,255,255,.08);

    border-radius:24px;

    padding:28px;

    box-shadow:
    0 10px 35px rgba(0,0,0,.35),
    inset 0 1px 0 rgba(255,255,255,.05);

    transition:.35s ease;
    margin-bottom:25px;
}

.subject-card:hover{

    transform:translateY(-6px);

    border:1px solid rgba(74,144,226,.4);

    box-shadow:
    0 18px 45px rgba(0,0,0,.45),
    0 0 25px rgba(74,144,226,.15);

}


.subject-card::before{

content:"";

position:absolute;

width:280px;
height:280px;

background:radial-gradient(circle,#3b82f655 0%,transparent 70%);

top:-140px;
right:-120px;

}


.header{

display:flex;
justify-content:space-between;
align-items:center;

margin-bottom:25px;

}


.subject-name{

font-size:28px;
font-weight:700;
color:white;

}


.badge{

background:#2563eb;

padding:7px 15px;

border-radius:999px;

font-size:13px;

font-weight:600;

color:white;

}


.code{

font-size:16px;

color:#94a3b8;

margin-top:8px;

}


.section{

margin-top:18px;

display:inline-block;

background:rgba(255,255,255,.08);

padding:8px 14px;

border-radius:10px;

font-size:14px;

color:white;

}


.stats-grid{

display:grid;

grid-template-columns:repeat(2,1fr);

gap:18px;

margin-top:28px;

}


.stat{

background:rgba(255,255,255,.05);

border-radius:18px;

padding:18px;

border:1px solid rgba(255,255,255,.05);

transition:.3s;

}


.stat:hover{

background:rgba(59,130,246,.15);

}


.stat-title{

font-size:13px;

color:#94a3b8;

margin-bottom:10px;

}


.stat-value{

font-size:28px;

font-weight:700;

color:white;

}


.footer{

margin-top:25px;

padding-top:18px;

border-top:1px solid rgba(255,255,255,.08);

}

</style>
""", unsafe_allow_html=True)

    html = f"""
<div class="subject-card">

<div class="header">

<div>

<div class="subject-name">
📘 {name}
</div>

<div class="code">
{code}
</div>

</div>

<div class="badge">
ACTIVE
</div>

</div>

<div class="section">
Section : {section}
</div>
"""

    if stats:

        html += '<div class="stats-grid">'

        for icon, key, value in stats:

            html += f"""

<div class="stat">

<div class="stat-title">

{icon}{key}

</div>

<div class="stat-value">

{value}

</div>

</div>

"""

        html += "</div>"

    html += """

<div class="footer">

</div>

</div>

"""

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()