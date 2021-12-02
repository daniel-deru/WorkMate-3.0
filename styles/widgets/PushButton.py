PushButton = """
    QPushButton {
    background-color: #000000;
    color: #ffffff;
    border: 2px solid #ffffff;
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
}

QPushButton:pressed {
    background-color: #ffffff;
    color: #000000;
    border: 2px solid #000000;
}
"""

CompleteButton = """
    QPushButton {
    background-color: transparent;
    font-size: 16px;
    image: url(assets/done.png);
    border: none;
    width: 60px;
}
"""

DeleteButton = """
    QPushButton {
    background-color: transparent;
    font-size: 16px;
    image: url(assets/delete.png);
    border: none;
    width: 50px;
}
"""