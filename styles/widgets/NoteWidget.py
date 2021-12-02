NoteWidget = """
    QFrame {
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        padding: 10px;
        background-color: #ffffff;
        color: #000000;
    }

    #lbl_name {
        color: #000000;
    }

    QPushButton {
        background-color: transparent;
        color: #ffffff;
        border: 2px solid #ffffff;
    }

    QPushButton#btn_edit {
        image: url(assets/edit.png);
        width: 20px;
        height: 20px;
        max-width: 20px;
        max-height: 20px;
    }

    QPushButton#btn_delete {
        image: url(assets/delete.png);
        width: 15px;
        height: 15px;
        max-width: 15px;
        max-height: 15px;
    }
"""

    # QPushButton::pressed {
    #     background-color: #ffffff;
    #     color: #000000;
    #     border: 2px solid #000000;
    # }