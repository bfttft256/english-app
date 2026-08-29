import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window

# 国立大学受験レベル（共通テスト〜二次試験）の出題データ
QUESTION_BANK = [
    {
        "question": "【暗号機解読 1/5】\n『reluctant』の意味として最も適切なものは？\n(例: He was reluctant to accept the offer.)",
        "options": ["気が進まない・嫌がる", "熱心な・鋭敏な", "不可欠な", "明白な"],
        "answer": 0
    },
    {
        "question": "【暗号機解読 2/5】\n『take A for granted』の正しい意味は？",
        "options": ["Aを当然のことと思う", "Aを諦める", "Aを考慮に入れる", "Aに感謝する"],
        "answer": 0
    },
    {
        "question": "【暗号機解読 3/5】\n『vulnerable』の意味として適切なものは？",
        "options": ["傷つきやすい・脆弱な", "価値がある", "多様な", "一時的な"],
        "answer": 0
    },
    {
        "question": "【暗号機解読 4/5】\n『It goes without saying that...』の意味は？",
        "options": ["〜は言うまでもない", "〜と言っても過言ではない", "〜することは不可能だ", "〜する価値がある"],
        "answer": 0
    },
    {
        "question": "【暗号機解読 5/5】\n『unprecedented』の意味として正しいものは？",
        "options": ["前例のない・空前の", "予期せぬ", "無制限の", "耐えがたい"],
        "answer": 0
    }
]

class CipherDecoderLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        self.current_q_index = 0
        self.progress = 0
        self.hunter_alert = 0
        
        self.status_label = Label(
            text="[暗号機解読率: 0%] ハンター判定: SAFE",
            font_size='18sp',
            size_hint_y=0.1
        )
        self.add_widget(self.status_label)
        
        self.pbar = ProgressBar(max=100, value=0, size_hint_y=0.05)
        self.add_widget(self.pbar)
        
        self.question_label = Label(
            text="",
            font_size='16sp',
            text_size=(Window.width - 40, None),
            halign='center',
            size_hint_y=0.3
        )
        self.add_widget(self.question_label)
        
        self.option_buttons = []
        for i in range(4):
            btn = Button(
                text="",
                font_size='16sp',
                size_hint_y=0.12,
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.bind(on_release=lambda instance, idx=i: self.check_answer(idx))
            self.option_buttons.append(btn)
            self.add_widget(btn)
            
        self.load_question()

    def load_question(self):
        if self.current_q_index < len(QUESTION_BANK):
            q_data = QUESTION_BANK[self.current_q_index]
            self.question_label.text = q_data["question"]
            opts = list(q_data["options"])
            for i, opt in enumerate(opts):
                self.option_buttons[i].text = opt
                self.option_buttons[i].disabled = False
        else:
            self.show_clear_screen()

    def check_answer(self, selected_idx):
        q_data = QUESTION_BANK[self.current_q_index]
        if selected_idx == q_data["answer"]:
            self.progress += 20
            self.pbar.value = self.progress
            self.current_q_index += 1
            if self.progress >= 100:
                self.show_clear_screen()
            else:
                self.status_label.text = f"[暗号機解読率: {self.progress}%] 判定成功！"
                self.load_question()
        else:
            self.hunter_alert += 1
            if self.hunter_alert >= 3:
                self.status_label.text = "【解読失敗】ハンターに捕獲されました！最初からやり直し。"
                self.reset_game()
            else:
                self.status_label.text = f"[暗号機解読率: {self.progress}%] 調整失敗！心音発生 (警告: {self.hunter_alert}/3)"

    def show_clear_screen(self):
        self.question_label.text = "【ゲート解放！脱出成功！】\n暗号機を全台解読しました。\n\n🎁 Element Sicks 報酬獲得！\n『The secret of success is constancy to purpose.』\n（初志貫徹こそが成功の鍵）"
        for btn in self.option_buttons:
            btn.disabled = True
        self.status_label.text = "【脱出成功】推しカード獲得！"

    def reset_game(self):
        self.current_q_index = 0
        self.progress = 0
        self.hunter_alert = 0
        self.pbar.value = 0
        self.load_question()

class IdentityEnglishApp(App):
    def build(self):
        return CipherDecoderLayout()

if __name__ == '__main__':
    IdentityEnglishApp().run()
