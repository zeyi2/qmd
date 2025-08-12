import argparse
import base64
import json
import re

def parse_qmd(qmd_path):
    """
    A simple (yet working) parser for QMD files.
    """
    questions = []
    with open(qmd_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('---')
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split('\n')
        question_text = lines[0].strip()
        options = {}
        for line in lines[1:]:
            line = line.strip()
            match = re.match(r'^([A-D])\.\s*(.*)', line, re.IGNORECASE)
            if match:
                options[match.group(1).upper()] = match.group(2).strip()

        questions.append({"question": question_text, "options": options})

    return questions

def parse_answers(answers_path):
    """
    Parse answers, mainly for judgement process.
    """
    with open(answers_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    answers = []
    parts = re.findall(r'\d+\.([A-D])', content, re.IGNORECASE)
    for part in parts:
        answers.append(part.upper())

    return answers

def generate_go_source(qmd_path, answers_path, template_path, output_path, phase_name):
    """
    Generate Go SRC File for compilation.
    """
    questions = parse_qmd(qmd_path)
    answers = parse_answers(answers_path)

    if len(questions) != len(answers):
        raise ValueError(
            f"Error: Number of questions ({len(questions)}) does not match number of answers ({len(answers)})."
        )

    data_to_embed = {
        "questions": questions,
        "correct_answers": answers
    }

    json_string = json.dumps(data_to_embed)
    # 防止小登拿 `strings` 命令作弊
    encoded_data = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    final_go_code = template_content.replace("{{ENCODED_DATA}}", encoded_data)
    final_go_code = final_go_code.replace("{{PHASE_NAME}}", phase_name)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_go_code)

    print(f"Successfully generated Go source: {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Go quiz source from QMD.")
    parser.add_argument("--qmd", required=True, help="Path to QMD file.")
    parser.add_argument("--answers", required=True, help="Path to answers file.")
    parser.add_argument("--template", required=True, help="Path to Go template file.")
    parser.add_argument("--output", required=True, help="Path for the output Go source file.")
    parser.add_argument("--phase", required=True, help="Name of the phase (e.g., phase-one).")

    args = parser.parse_args()

    generate_go_source(args.qmd, args.answers, args.template, args.output, args.phase)
