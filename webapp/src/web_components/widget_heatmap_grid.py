from calendar import month_name
import streamlit as st
import streamlit.components.v1 as components
from pandas import DataFrame

def show_heatmap_grid_widget(title, year, month, header, rows,
                             threshold_low=1, threshold_medium=2, threshold_high=3):
    """ Renders a heat map grid
    
        header - header columns
        rows - list of rows
    """

    st.header(f"{title} ({month_name[month]} {year})")

    html = """
    <style>
        .gridComponent {
            font-family: "Verdana", sans-serif;
            font-size: 12px;

            align: center;
        }
        .gridComponent table {
            width: 100%;
            border-collapse: collapse;
            align: center;
        }
        .gridComponent tr td {
            border-width: 1px;
            border-style: solid;
            border-color: black;
            padding: 0;
            margin: 0;
            border-spacing: 0;
            text-align: center;
        }
        .gridComponent td {
            width: 25px;
            white-space: nowrap;
        }
        .gridStrong {
            font-weight: bold;
        }
        .gridComponent thead {
            background-color: black;
            color: white;
        }
        .gridCellHigh {
            background-color: red;
        }
        .gridCellMedium {
            background-color: yellow;
        }
        .gridCellLow {
            background-color: green;
        }
    </style>
    <div id="grid" class="gridComponent">
        <table>
    """
    
    # display header
    if header is not None and len(header) > 0:
        html += """
        <thead>
            <tr>
        """
        for h in header:
            html += f"<td>{h}</td>"
        html += """
            </tr>
        </thead>
        """

    # display rows
    if rows is not None and len(rows) > 0:
        html += """
        <tbody>
        """
        for r in rows:
            html += "<tr>"
            for i in range(len(r)):
                val_str = ""
                val_class = ""
                val = r[i]

                # trailing column
                if i == (len(r) - 1):
                    val_class = " class=\"gridStrong\""
                    if val is not None:
                        val_str = val

                # number
                elif val is not None and (type(val) == int or \
                    (type(val) == str and val.isdigit())):
                    val_str = val
                    if int(val) >= threshold_high:
                        val_class = " class=\"gridCellHigh\""
                    elif int(val) >= threshold_medium:
                        val_class = " class=\"gridCellMedium\""
                    elif int(val) >= threshold_low:
                        val_class = " class=\"gridCellLow\""
            
                # string
                elif val is not None:
                    val_str = val

                html += f"<td{val_class}>{val_str}</td>"
            html += "</tr>"
        html += """
        </tbody>
        """
    
    # close out html
    html += """
        </table>
    </div>
    """
    
    components.html(html, height=600)
