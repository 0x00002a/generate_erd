import datetime


def format_erd(tbls, links, out):
    out("""
        /* Generated on {}, by generate_erd.py, a script written by Natasha
        England-Elbro */
            """.format(datetime.date.today()))
    out("""
        digraph {
            graph[overlap=false, splines=true, rankdir="LR"];
            node[shape=record];
            ranksep=2;


            """)
    for tbl in tbls:
        out("{}[shape=none, margin=0, label=<".format(tbl.name))
        out("<table border='0' cellborder='1' cellspacing='0' cellpadding='4'>")
        out("<tr><td bgcolor=\"lightblue\">{0}</td></tr>".format(tbl.name))

        for col in tbl.cols:
            out("<tr><td align=\"left\" port='{0}'>{0}: {1}</td></tr>".format(col.name,
                                                                              col.dtype))
        out("""</table>
        >];""")

    for link in links:
        out("{0}:{1} -> {2}:{3}".format(link.src_tbl.name, link.src_col.name,
                                        link.dest_tbl.name, link.dest_col.name))

    out("}")
