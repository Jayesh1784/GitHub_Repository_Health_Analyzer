import json
import os

class ReportGenerator:
    def generate(self, data, filename="report.json", output_format="json"):
        # Save to project root (two levels up from this file)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_path = os.path.join(project_root, filename)

        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Report saved: {output_path}")
