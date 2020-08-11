import json
import os


class JsonlExporter:

    def __init__(self, path='../files/'):
        self.folder_path = os.path.join(os.path.dirname(__file__), path)

    def export(self, data, name):
        mode = 'a+'
        out_put_path = self.folder_path+name+'.jsonl'

        self.__create_files_dir_if_not_exists()

        with open(file=out_put_path, mode=mode, encoding='utf-8') as f:
            for line in data['data']:
                json_record = json.dumps(line, ensure_ascii=False)
                f.write(json_record + '\n')
        return True

    def __create_files_dir_if_not_exists(self):
        if not os.path.isdir(self.folder_path):
            os.mkdir(self.folder_path)
