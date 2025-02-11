def populate_tree(tree, data, filter_value=None):
    for row in tree.get_children():
        tree.delete(row)

    tree["columns"] = data[0]
    tree["show"] = "headings"

    for col in data[0]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    try:
        month_col_index = data[0].index("Betreuungsmonat")
    except ValueError:
        month_col_index = None

    for row in data[1:]:
        if not filter_value or (month_col_index is not None and row[month_col_index] == filter_value):
            tree.insert("", "end", values=row)
