import streamlit as st
import pandas as pd
from streamlit import session_state as ss
import scanpy as sc
import json
from helpers.file_handling import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def showSGR():
    singleron_base64 = read_image("src/singleron.png")
    with st.sidebar:
        st.markdown("---")

        st.markdown(
            f'<div style="margin-top: 0.25em; text-align: left;"><a href="https://singleron.bio/" target="_blank"><img src="data:image/png;base64,{singleron_base64}" alt="Homepage" style="object-fit: contain; max-width: 174px; max-height: 41px;"></a></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '''
            sessupport@singleronbio.com
            '''
        )

def binaryswitch(session_state, keys):
    for key in keys:
        if session_state[key] is True:
            session_state[key] = False
        else:
            session_state[key] = True

def toFalse(session_state, keys):
    for key in keys:
        session_state[key] = False

### 画图函数
def plot4spa(adata_list, celltype_chosen, numL):
    x_width  = []
    y_height = []
    for lable in adata_list:
        adata          = adata_list[lable]
        x_width    += [max(adata.obs["x"] - min(adata.obs["x"]))]
        y_height   += [max(adata.obs["y"] - min(adata.obs["y"]))]
    
    p_width    = max(x_width) * 1.05
    p_height   = max(y_height) * 1.2
    lab_x_off  = -0.05   *  p_width
    lab_y_off  = - p_height/2
    total      = len(adata_list)
    lables     = list(adata_list.keys())
    
    ## 按3个分成多少行
    rlist = [min(numL, total - i * numL) for i in range((total - 1) // numL + 1)]
    fig = make_subplots(rows=1, cols=1)
    
    ## 根据celltype来画图：
    for celltype in sorted(celltype_chosen.keys()):
        if not celltype_chosen[celltype]:
            continue
        cx = pd.Series([])
        cy = pd.Series([])
        ct = pd.Series([])
        add_lable = False
        ## 代表横坐标
        for i in range(1, numL+1):
            ## 代表纵坐标
            for j in range(len(rlist)):
                index = i + j * numL
                if index <= total:
                    lable  = lables[index-1]
                    adata = adata_list[lable]
                    df      = adata.obs[adata.obs["cell_type"] == celltype]
                    if df.empty:
                        continue
                    x_off  = (i-1) * p_width
                    y_off  = -1 * j * p_height
                    if ct.empty:
                        cx = df["x"]+x_off
                        cy = df["y"]+y_off
                        ct  = df["cell_type"]                        
                    else:
                        cx = pd.concat([cx,   df["x"]+x_off])
                        cy = pd.concat([cy,   df["y"]+y_off])
                        ct  =  pd.concat([ct,  df["cell_type"]])
                ## 添加子标题
                if not add_lable:
                    fig.add_annotation(
                        x= x_off    + lab_x_off,  # 指定 x 位置
                        y= y_off    + lab_y_off,  # 指定 y 位置
                        text=lable,  # 要写入的文字内容
                        showarrow=False,  # 是否显示箭头
                        font=dict(color="black", size=12),  # 文字的样式
                    )
        add_lable = True
       ## 添加细胞类型
        fig.add_trace(
            go.Scatter(x=cx, 
                       y=cy,
                      mode='markers',
                      marker=dict( color=ss["celltype_colours"][celltype] , size=3.5),
                      name=celltype,
                      text=ct,  # 使用 'text' 列的值作为提示信息
                      hoverinfo='text'  # 显示 text 参数中的信息
            ),
            row=1, col=1
        )

    # 创建一个空白的布局
    layout = go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',  # 设置背景颜色为透明
        paper_bgcolor='rgba(0,0,0,0)',  # 设置绘图区域的背景颜色为透明
        xaxis=dict(visible=False),  # 隐藏 x 轴
        yaxis=dict(visible=False)  # 隐藏 y 轴
    )
    #fig.update_layout(height=600, width=1500, title_text="Position of annotated cells in embryo tissue", title_x=0.5)
    fig.update_layout(
        legend_title_text="cell types",
    )

    fig.update_layout(layout)
    return fig

def cell_type_check(numL):
    total = len(ss.celltype_colours)
    names = sorted(ss.celltype_colours)
    rlist = [min(numL, total - i * numL) for i in range((total - 1) // numL + 1)]
    cols  = st.columns([1]*numL)
    # 设置每一个列的空隔为0
    st.markdown(
    """
        <style>[data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{ gap: 0rem; }</style>
        <style>[data-testid=column]:nth-of-type(2) [data-testid=stVerticalBlock]{ gap: 0rem; }</style>
        <style>[data-testid=column]:nth-of-type(3) [data-testid=stVerticalBlock]{ gap: 0rem; }</style>
        <style>[data-testid=column]:nth-of-type(4) [data-testid=stVerticalBlock]{ gap: 0rem; }</style>
        <style>[data-testid=column]:nth-of-type(5) [data-testid=stVerticalBlock]{ gap: 0rem; }</style>
    """,unsafe_allow_html=True)

    for i in range(1, numL+1):
        for j in range(len(rlist)):
            index = i + j * numL
            if index <= total:
                cols[i-1].checkbox(names[index-1], value=ss.celltype_chosen[names[index-1]], on_change=binaryswitch, args = (ss.celltype_chosen, [names[index-1]],))

def main():
    # initial variables
    default_variables = {
        "showData": False,
        "running": False,
        "zipResults": False,
        "showVolca": False,
        "showTable": False,
        "dataOK": False,
        "dataSource": None,
        "group1": None,
        "group2": None,
        "checkSPA":False,
        "celltype_colours":{},
        "celltype_chosen" :{},
        "init_colours": False,
        "chekc_celltype": False,
        "adata_list":{}
    }
    for key, value in default_variables.items():
        if key not in st.session_state:
            ss[key] = value

    ## 设置页面宽一些
    st.set_page_config(layout="wide")
    st.sidebar.markdown("# SageNet")
    st.sidebar.markdown("## 1.Inputs")

    input_selectbox = st.sidebar.selectbox(
        "What data would you like to use for analysis?",
        ("mouse embryo", "Upload new"),
        index=None, placeholder="Please select ..."
    )
    if input_selectbox is None:
        st.title("Welcome !!!")
        st.write("Please select the inputs from the right slidebar!")
        showSGR()
        st.stop()

    if input_selectbox == "mouse embryo":
        input_files = pd.DataFrame({
            "Lable":["Embryo1.1", "Embryo1.2", "Embryo1.3", "Embryo2.1", "Embryo2.2", "Embryo2.3", "scRNA_seq1"],
            "Source":["Lohoff et al. (2022)"]*6 + ["Pijuan-Sala et al. (2019)"],
            "Datatype":["seqFISH"]*6 + ["scRNA-seq"],
        })
        lable_file = {
            "Embryo1.1"  : "./demo/mouse_embryo/adata_seqFISH1_1.h5ad",
            "Embryo1.2"  : "./demo/mouse_embryo/adata_seqFISH1_2.h5ad",
            "Embryo2.1"  : "./demo/mouse_embryo/adata_seqFISH2_1.h5ad",
            "Embryo2.2"  : "./demo/mouse_embryo/adata_seqFISH2_2.h5ad",
            "Embryo1.3"  : "./demo/mouse_embryo/adata_seqFISH3_1.h5ad",
            "Embryo2.3"  : "./demo/mouse_embryo/adata_seqFISH3_2.h5ad",
            "scRNA_seq1" : "./demo/mouse_embryo/adata_scRNAseq.h5ad"
        } 
        ss['dataSource'] = "mouse embryo"
        st.session_state["dataOK"] = True

    else:
        st.subheader("Upload your RNA-Seq data (h5ad format)")
        exp_file  = st.file_uploader("Choose a h5ad file for gene expression",   type="csv", disabled=True)
        #st.write("Note: The first column of the matrix contains gene names, followed by the expression matrix of each sample, with column names representing the sample names.")
        spa_file = st.file_uploader("Choose a h5ad file for Spatial Transcriptomics", type="csv", disabled=True)
        #st.write("Note: This file contains grouping information. The first column is the sample name, with column name \"sample\". The values in the first column correspond to the expression matrix of the samples mentioned earlier. The second column contains grouping information with column name \"group\".")

    if ss["dataOK"] == True:
        if not ss['checkSPA']:
            st.write("Data info:")
            st.write(input_files)
            st.write("Now you can select spatial transcriptomics data from the left sidebar for viewing and model training.:")
    else:
        st.stop()

    # Running
    st.sidebar.markdown("## 2.Running")
    ## 选择空间转录组样品
    spa_samples     = input_files[input_files['Datatype'] != "scRNA-seq"]["Lable"].tolist()
    spa_samples_sel = st.sidebar.multiselect(
        '2.1Spatial transcriptomics samples:',
        spa_samples,
        on_change=toFalse,
        args = (ss, ['checkSPA', "init_colours", "chekc_celltype"]) # 只要这个动了，下面就是False了
    )


    chekc_spa = st.sidebar.checkbox("Confirm ST selection", value=ss['checkSPA'], on_change=binaryswitch, args = (ss, ['checkSPA', "init_colours"]))

    if not ss['checkSPA'] or len(spa_samples_sel) <=0:
        st.stop()
    else:
        st.write("You have chosen datas:")
        st.write(input_files[input_files['Lable'].isin(spa_samples_sel)])


        ## 只有在第一次确认了samples的时候才读入
        if ss["init_colours"]:
            plot_celltype = set()
            ss.adata_list = {}
            for sample in spa_samples_sel:
                print(sample)
                adata = sc.read_h5ad(lable_file[sample])
                ss.adata_list[sample] = adata
                plot_celltype         = plot_celltype.union( set(adata.obs["cell_type"].unique()) )

            with open("celltype_colours.json", 'r') as json_file:
                ss.celltype_colours = json.load(json_file)
                ss.celltype_colours = {key: ss.celltype_colours[key] for key in ss.celltype_colours if key in plot_celltype}
                ss.celltype_chosen  = {key:True for key in ss.celltype_colours}
                ss["init_colours"]  = False

        
        ## 默认全选所有的细胞类型
        st.markdown("---")
        st.markdown("""
        **Firstly**, you can select to display or hide relevant data by clicking on the cell type names in the legends below, which will help you to view the data more clearly and decide which cell types to include in further analysis. 
        """)
        fig_spa = plot4spa(ss.adata_list, ss.celltype_chosen, 3)
        st.plotly_chart(fig_spa, use_container_width=True)
        st.markdown("""
        **Secondly**, once you have decided which cell types to exclude, please uncheck the relevant checkboxes below and then click the \"Confirm celltype selection\" from the **lefe slidebar**.
        """)
        cell_type_check(4) # 每一行是4个细胞名字

        ## 确认选择的细胞类型
        chekc_celltype = st.sidebar.checkbox("Confirm celltype selection", value=ss['chekc_celltype'], on_change=binaryswitch, args = (ss, ['chekc_celltype']))
        

        #if ss["chekc_celltype"]:



    st.sidebar.markdown("### Tables")
    st.sidebar.markdown("### Plots")

    st.sidebar.markdown("### Citations")

    st.markdown("---")
    st.markdown(
        '''
        ### Citations:
         * [scArches](https://docs.scarches.org/en/latest/about.html): Lotfollahi M, Naghipourfar M, Luecken M D, et al. Mapping single-cell data to reference atlases by transfer learning[J]. Nature biotechnology, 2022, 40(1): 121-130.
         * [SageNet](https://github.com/MarioniLab/sagenet): Heidari E, Lohoff T, Tyser R C V, et al. Supervised spatial inference of dissociated single-cell data with SageNet[J]. bioRxiv, 2022: 2022.04. 14.488419.
         * Lohoff T, Ghazanfar S, Missarova A, et al. Integration of spatial and single-cell transcriptomic data elucidates mouse organogenesis[J]. Nature biotechnology, 2022, 40(1): 74-85.
        '''
    )



if __name__ == "__main__":
    main()
