import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QFileDialog, QScrollArea, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt

class CaseStudyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load block-variable mapping
        with open('BLOCK_VARIABLE_LIST.json', 'r', encoding='utf-8') as f:
            self.var_map = json.load(f)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Aspen Case Study GUI")
        self.setFixedSize(600, 900)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        
        # Global config
        config_section = QWidget()
        config_form = QFormLayout(config_section)
        self.file_edit = QLineEdit()
        self.output_name = QLineEdit()
        self.log_path = QLineEdit("./")
        self.visible_combo = QComboBox(); self.visible_combo.addItems(["False","True"])
        self.reset_combo = QComboBox(); self.reset_combo.addItems(["True","False"])
        self.retry_spin = QSpinBox(); self.retry_spin.setValue(3)
        self.unit_edit = QLineEdit("200")
        config_form.addRow("Aspen File:", self.file_edit)
        config_form.addRow("Output Name:", self.output_name)
        config_form.addRow("Log File Path:", self.log_path)
        config_form.addRow("Visible:", self.visible_combo)
        config_form.addRow("Reset Params:", self.reset_combo)
        config_form.addRow("Retry Attempts:", self.retry_spin)
        config_form.addRow("Output Unit Count:", self.unit_edit)
        layout.addWidget(config_section)

        # Input section
        add_case_btn = QPushButton("+ Add Case Target")
        add_case_btn.clicked.connect(self.add_case_row)
        layout.addWidget(add_case_btn)
        self.case_container = QWidget()
        self.case_layout = QVBoxLayout(self.case_container)
        case_scroll = QScrollArea(); case_scroll.setWidgetResizable(True); case_scroll.setWidget(self.case_container)
        layout.addWidget(case_scroll, 1)

        # Output section
        add_out_btn = QPushButton("+ Add Output Field")
        add_out_btn.clicked.connect(self.add_out_row)
        layout.addWidget(add_out_btn)
        self.out_container = QWidget()
        self.out_layout = QVBoxLayout(self.out_container)
        out_scroll = QScrollArea(); out_scroll.setWidgetResizable(True); out_scroll.setWidget(self.out_container)
        layout.addWidget(out_scroll, 1)

        submit_btn = QPushButton("Submit to JSON")
        submit_btn.clicked.connect(self.submit_to_json)
        layout.addWidget(submit_btn)

        self.setCentralWidget(central)

    def add_case_row(self):
        row = QWidget(); hl = QHBoxLayout(row)
        blk_combo = QComboBox(); blk_combo.addItems(self.var_map['INPUT'].keys())
        blk_name = QLineEdit()
        var_combo = QComboBox()
        sub_input = QLineEdit(); sub_input.setPlaceholderText('Enter value'); sub_input.setVisible(False)
        instr = QTextEdit(); instr.setFixedHeight(30); instr.setPlaceholderText('Instruction')

        def on_block_change(idx):
            var_combo.clear()
            for item in self.var_map['INPUT'][blk_combo.currentText()]:
                var_combo.addItem(item['description'], item)
        blk_combo.currentIndexChanged.connect(on_block_change)

        def on_var_change(idx):
            sub_input.setVisible(False)
            item = var_combo.currentData()
            if not isinstance(item, dict): return
            for key, val in item.items():
                if key.startswith('variable') and isinstance(val, str) and val.startswith('<') and val.endswith('>'):
                    sub_input.setVisible(True)
                    sub_input.setPlaceholderText(val)
                    break
        var_combo.currentIndexChanged.connect(on_var_change)

        hl.addWidget(blk_combo); hl.addWidget(blk_name)
        hl.addWidget(var_combo); hl.addWidget(sub_input); hl.addWidget(instr)
        self.case_layout.addWidget(row)
        on_block_change(0)

    def add_out_row(self):
        row = QWidget(); hl = QHBoxLayout(row)
        blk_combo = QComboBox(); blk_combo.addItems(self.var_map['OUTPUT'].keys())
        blk_name = QLineEdit()
        var_combo = QComboBox()
        sub_input = QLineEdit(); sub_input.setPlaceholderText('Enter value'); sub_input.setVisible(False)

        def on_block_change(idx):
            var_combo.clear()
            for item in self.var_map['OUTPUT'][blk_combo.currentText()]:
                var_combo.addItem(item['description'], item)
        blk_combo.currentIndexChanged.connect(on_block_change)

        def on_var_change(idx):
            sub_input.setVisible(False)
            item = var_combo.currentData()
            if not isinstance(item, dict): return
            for key, val in item.items():
                if key.startswith('variable') and isinstance(val, str) and val.startswith('<') and val.endswith('>'):
                    sub_input.setVisible(True)
                    sub_input.setPlaceholderText(val)
                    break
        var_combo.currentIndexChanged.connect(on_var_change)

        hl.addWidget(blk_combo); hl.addWidget(blk_name)
        hl.addWidget(var_combo); hl.addWidget(sub_input)
        self.out_layout.addWidget(row)
        on_block_change(0)

    def submit_to_json(self):
        data = {'config':{}, 'cases':[], 'outputs':[]}
        data['config'] = {
            'aspen_file': self.file_edit.text(),
            'output_name': self.output_name.text(),
            'log_path': self.log_path.text(),
            'visible': self.visible_combo.currentText(),
            'reset_params': self.reset_combo.currentText(),
            'retry_attempts': self.retry_spin.value(),
            'unit_count': int(self.unit_edit.text())
        }
        for i in range(self.case_layout.count()):
            w = self.case_layout.itemAt(i).widget()
            bt = w.layout().itemAt(0).widget().currentText()
            bn = w.layout().itemAt(1).widget().text()
            cv = w.layout().itemAt(2).widget()
            item = cv.currentData()
            sub = w.layout().itemAt(3).widget().text()
            instr = w.layout().itemAt(4).widget().toPlainText()
            entry = {'block_type': bt, 'block_name': bn, 'input_type': cv.currentText(), 'instruction': instr}
            if sub: entry['sub_input'] = sub
            # build variable_path
            if bt == 'Stream':
                prefix = f'AspenSimulation.Tree.Elements("Data").Elements("Streams").Elements("{bn}").Elements("Input")'
            else:
                prefix = f'AspenSimulation.Tree.Elements("Data").Elements("Blocks").Elements("{bn}").Elements("Input")'
            path = prefix
            if isinstance(item, dict):
                for key in sorted(item):
                    if key.startswith('variable'):
                        val = item[key]
                        if val.startswith('<') and val.endswith('>'):
                            vn = sub
                        else:
                            vn = val
                        path += f'.Elements("{vn}")'
            path += '.Value'
            entry['variable_path'] = path
            data['cases'].append(entry)
        for i in range(self.out_layout.count()):
            w = self.out_layout.itemAt(i).widget()
            bt = w.layout().itemAt(0).widget().currentText()
            bn = w.layout().itemAt(1).widget().text()
            cv = w.layout().itemAt(2).widget()
            item = cv.currentData()
            sub = w.layout().itemAt(3).widget().text()
            entry = {'block_type': bt, 'block_name': bn, 'output_type': cv.currentText()}
            if sub: entry['sub_input'] = sub
            if bt == 'StreamOutput':
                prefix = f'AspenSimulation.Tree.Elements("Data").Elements("Streams").Elements("{bn}").Elements("Output")'
            else:
                prefix = f'AspenSimulation.Tree.Elements("Data").Elements("Blocks").Elements("{bn}").Elements("Output")'
            path = prefix
            if isinstance(item, dict):
                for key in sorted(item):
                    if key.startswith('variable'):
                        val = item[key]
                        if val.startswith('<') and val.endswith('>'):
                            vn = sub
                        else:
                            vn = val
                        path += f'.Elements("{vn}")'
            path += '.Value'
            entry['variable_path'] = path
            data['outputs'].append(entry)
        fn,_ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON Files (*.json)")
        if fn:
            with open(fn, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "Saved", f"Config saved to {fn}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = CaseStudyGUI()
    gui.show()
    sys.exit(app.exec_())