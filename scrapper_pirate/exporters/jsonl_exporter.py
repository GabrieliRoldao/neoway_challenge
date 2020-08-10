import json
import os

FOLDER_PATH = os.path.join(os.path.dirname(__file__), '../files/')


class JsonlExporter:

    def export(self, data, name):
        mode = 'a+'
        out_put_path = FOLDER_PATH+name+'.jsonl'
        with open(file=out_put_path, mode=mode, encoding='utf-8') as f:
            for line in data['data']:
                json_record = json.dumps(line, ensure_ascii=False)
                f.write(json_record + '\n')
        return True
