import json
import os

class ReportGenerator:
    def generate(self, data, filename="report.json", output_format="json"):
        # Always save to the project root, not the cloned repo folder
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(project_root, filename)

        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Report saved: {output_path}")
