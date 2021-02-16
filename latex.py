
def format_erd(tbls, links, out):
    def p_db_table(tbl):
        out(r"""
                \begin{table*}
                \caption{Fields of %s}\label{table:fields:%s}
            \centering
            \begin{tabularx}{\textwidth}{XXXXXX}
                    \toprule
                    \textbf{Field name} & \textbf{Data type}  &
                    \textbf{Example}    & \textbf{Validation} & \textbf{Description} &
                    \textbf{Foreign key}                                               \\
                    \midrule
            """ % (tbl.name, tbl.name))
        for col in tbl.cols:
            is_fk = bool([x for x in links if x.src_tbl == tbl and x.src_col ==
                          col])
            out(r"{0} & {1} & N/A & N/A & N/A & {2} \\".format(col.name,
                                                               col.dtype.lower(),
                                                               is_fk))
        out(r"""
\bottomrule
\end{tabularx}
\end{table*}
        """)
    for t in tbls:
        p_db_table(t)
