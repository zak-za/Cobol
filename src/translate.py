import re


"""Translation operations"""


def handle_header(line: str) -> str:
    """Perform translation on PERFORM line

    Args:
        line (str)

    Returns:
        str
    """

    return f"En el párrafo {line} :"


def handle_perform(line: str) -> str:
    """Perform translation on PERFORM line

    Args:
        line (str)

    Returns:
        str
    """

    words = line.split()
    return f"Se invoca al párrafo {words[1] if len(words) else ''}"


def handle_call(line: str) -> str:
    """Perform translation on CALL line

    Args:
        line (str)

    Returns:
        str
    """

    words = line.split("USING")
    first_part = words[0].split()[1].strip().lstrip() if len(words) else ""
    return f"Se obtiene la fecha del día ({first_part}) a través de la rutina DSPCMCTR usando la copy {words[1]}"


def handle_intialize(line: str) -> str:
    """initialize translation on CALL line

    Args:
        line (str)

    Returns:
        str
    """

    words = line.split()
    return f"Se inicializa el variable {words[1]}"


def handle_set(line: str) -> str:
    """set translation on CALL line

    Args:
        line (str)

    Returns:
        str
    """
    
    translate = ""
    words = line.split()
    translate = f"Se activa el switch {words[1]}"
    return translate


def handle_add(line: str) -> str:
    """ADD translation on CALL line

    Args:
        line (str)

    Returns:
        str
    """

    words = line.split()
    return f"Se añade {words[1]} al índice {words[3]}"


def handle_read(line: str) -> str:
    """read translation on CALL line

    Args:
        line (str)

    Returns:
        str
    """
    
    words = line.split('INTO')
    if len(words):
        temp = words[0].split(' ', 1)
        if len(temp):
            return f"Se lee el fichero de entrada {temp[1].strip().lstrip()} con la copy {words[1].strip().lstrip()}"
    return ""


def handle_open(line: str) -> str:
    """open translation on CALL line

    Args:
        line (str)

    Returns:
        str
    """

    return ""


def handle_compute(line: str) -> str:
    """ADD translation on CALL line

    Args:
        line (str)

    Returns:
        str
    """

    return ""


def handle_into(line: str) -> str:
    """if translation on CALL line

    Args:
        line (str)

    Returns:
        str
    """

    return ""


def handle_if(doc, line: str) -> str:
    """if translation on CALL line

    Args:
        line (str)

    Returns:
        str
    """
    
    words = line.split("<br />")
    temp = ''
    
    for word in words:
        tmp = word.split()
        # --------------------- Handle IF line
        if 'ELSE' in word:
            pass
        elif 'NOT EQUAL' in word:
            if len(tmp):
                doc.add_unordered_list(f"Si el campo de retorno {tmp[1].strip().lstrip()} no es igual a cero")
        elif 'EQUAL' in word:
            if len(tmp):
                doc.add_unordered_list(f"Si el campo de retorno {tmp[1].strip().lstrip()} no es igual a cero")
        elif 'NO-' in word:
            if len(tmp):
                temp = tmp[1].strip().lstrip()
                
        # --------------------- Handle other lines
        translation = ''
        if "PERFORM" in word:
            translation = f"Si {temp} {handle_perform(line=word)}" if handle_perform(line=word) != "" else ''
        elif "MOVE" in word:
            handle_move(doc=doc, line=word)
        elif "INITIALIZE" in word:
            translation = f"Si {temp} {handle_intialize(line=word)}" if handle_intialize(line=word) != "" else ''
            
            
        if translation != "":
            print(translation)
            doc.add_unordered_list(translation)
            
    return ""


def handle_move(doc, line: str) -> str:
    """if translation on MOVE line

    Args:
        line (str)

    Returns:
        str
    """
    
    moves = line.split("<br />")
    non_breaking_space_pattern = re.compile(r'\xa0')
    empty_line_pattern = re.compile(r'^\s*$')
    pattern = r"MOVE\s+(.*?)\s+TO\s+(.*)"
    tmp = [["Campo Origen", "Campo Destino"]]
    for move in moves:
        cleaned_line = non_breaking_space_pattern.sub(' ', move).strip()
        cleaned_line = move.strip()
        if empty_line_pattern.match(cleaned_line):
            continue
        if not cleaned_line:
            continue
        match = re.search(pattern, cleaned_line)
        if match:
            org = match.group(1).strip()
            des = match.group(2).strip()
            tp = [org, des]
            tmp.append(tp)
    doc.add_unordered_list(f"Se informan los siguientes campos:")
    doc.add_table(tmp, rows=len(tmp), cols=2)
    return ""


def translate(doc, word: str, line: str = ""):
    """Perform translations on line

    Args:
        word (Document)
        word (str)
        line (str, optional)

    Returns:
        str
    """
    
    translation = ""

    if "PERFORM" == word:
        translation = handle_perform(line=line)
    elif "CALL" == word:
        translation = handle_call(line=line)
    elif "INITIALIZE" == word:
        translation = handle_intialize(line=line)
    elif "SET" == word:
        translation = handle_set(line=line)
    elif "OPEN" == word:
        translation = handle_open(line=line)
    elif "ADD" == word:
        translation = handle_add(line=line)
    elif "COMPUTE" == word:
        translation = handle_compute(line=line)
    elif "READ" == word:
        translation = handle_read(line=line)
    elif "IF" == word:
        handle_if(doc, line=line)
    elif "MOVE" == word:
        handle_move(doc, line=line)

    if translation != "":
        doc.add_unordered_list(translation)
