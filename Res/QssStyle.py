red_light_style = '''QPushButton{background:#F76677;border-radius:8px;margin:6px;}#QPushButton:hover{background:red;}'''
yellow_light_style = '''QPushButton{background:#F7D674;border-radius:8px;margin:6px;}#QPushButton:hover{background:yellow;}'''
green_light_style = '''QPushButton{background:#6DDF6D;border-radius:8px;margin:6px;}#QPushButton:hover{background:green;}'''
list_tab_style = '''QListWidget{padding-top:12px;border:1px solid lightgray; color:white; background:#0046A5;font-size:15pt;font-family: '新宋体';}
                QListWidget::Item{padding-top:0px; padding-bottom:0px; }
                QListWidget::Item:hover{background:white;color:gray }
                QListWidget::item:selected{background:wheat; color:white; }
                QListWidget::item:selected:!active{border-width:0px; background:lightgray; color:dark;}'''
list_cmd_style = '''QListWidget{border:0px solid white;color:white;font-size:14pt;font-family: "新宋体";background:lightgray}
                QListWidget::Item{background:#0046A5; }
                QListWidget::Item:hover{background:#004680; }
                QListWidget::item:selected{background:#004680; color:white; }'''
list_cmd_menu_style = "QMenu{\
            background-color:#3346A5; /* sets background of the menu 设置整个菜单区域的背景色，我用的是白色：white*/\
            border: 1px solid white;/*整个菜单区域的边框粗细、样式、颜色*/\
        }\
        QMenu#item {\
            /* sets background of menu item. set this to something non-transparent\
                if you want menu color and menu item color to be different */\
            background-color: transparent;\
            padding:8px 32px;/*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/\
            margin:0px 8px;/*设置菜单项的外边距*/\
            border-bottom:1px solid #DBDBDB;/*为菜单项之间添加横线间隔*/\
        }\
        QMenu#item:selected { /* when user selects item using mouse or keyboard */\
            background-color: #2dabf9;/*这一句是设置菜单项鼠标经过选中的样式*/\
        }"
