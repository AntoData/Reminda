import sys
sys.path.append("./UIClasses")
sys.path.append("./BE-Logic")
sys.path.append("./Config")
import main_window
import LoggerMeta
import load_questions_window
from create_questionnaire_start import CreateQuestionnaire
from window_design import SimpleWindow
from config_pop_up import ConfigPopUp

main_window.MainWindow().window.mainloop()