import uno
    
class LibreOfficeHandler:

    def __init__(self):

        self.ctx = None
        self.smgr = None
        self.desktop = None

        self.document = None
        self.sheet = None

        ###################################################
        # INTERNAL CURSOR TRACKING
        ###################################################

        self.current_row = 0
        self.current_col = 0

        ###################################################
        # SETTINGS
        ###################################################

        self.direction = "right"

        self.skip_filled = False

    ###################################################
    # CONNECT TO LIBREOFFICE
    ###################################################

    def connect(self):

        local_ctx = uno.getComponentContext()

        resolver = local_ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver",
            local_ctx
        )

        self.ctx = resolver.resolve(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
        )

        self.smgr = self.ctx.ServiceManager

        self.desktop = self.smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop",
            self.ctx
        )

    ###################################################
    # CREATE DOCUMENT
    ###################################################

    def create_document(self):

        self.document = self.desktop.loadComponentFromURL(
            "private:factory/scalc",
            "_blank",
            0,
            ()
        )

        self.sheet = self.document.Sheets.getByIndex(0)

        self.current_row = 0
        self.current_col = 0

    ###################################################
    # OPEN DOCUMENT
    ###################################################

    def open_document(self, path):

        file_url = uno.systemPathToFileUrl(path)

        self.document = self.desktop.loadComponentFromURL(
            file_url,
            "_blank",
            0,
            ()
        )

        self.sheet = self.document.Sheets.getByIndex(0)

        self.current_row = 0
        self.current_col = 0

    ###################################################
    # SAVE
    ###################################################

    def save(self):

        if self.document:

            self.document.store()

    ###################################################
    # WRITE TO CURRENT CELL
    ###################################################

    def write_current_cell(self, text):

        cell = self.sheet.getCellByPosition(
            self.current_col,
            self.current_row
        )

        cell.setString(text)

        self.highlight_current_cell()

        self.save()

    ###################################################
    # READ CELL
    ###################################################

    def get_cell_text(self, col, row):

        cell = self.sheet.getCellByPosition(
            col,
            row
        )

        return cell.getString()

    ###################################################
    # AUTO MOVEMENT
    ###################################################

    def move_next(self):

        if self.direction == "right":

            self.current_col += 1

        elif self.direction == "left":

            if self.current_col > 0:
                self.current_col -= 1

        elif self.direction == "down":

            self.current_row += 1

        elif self.direction == "up":

            if self.current_row > 0:
                self.current_row -= 1

        ###################################################
        # OPTIONAL SKIP FILLED CELLS
        ###################################################

        if self.skip_filled:

            self.skip_used_cells()

        self.highlight_current_cell()

    ###################################################
    # SKIP FILLED CELLS
    ###################################################

    def skip_used_cells(self):

        max_attempts = 1000

        attempts = 0

        while attempts < max_attempts:

            text = self.get_cell_text(
                self.current_col,
                self.current_row
            )

            if text.strip() == "":
                return

            ###################################################
            # MOVE AGAIN
            ###################################################

            if self.direction == "right":

                self.current_col += 1

            elif self.direction == "left":

                if self.current_col > 0:
                    self.current_col -= 1

            elif self.direction == "down":

                self.current_row += 1

            elif self.direction == "up":

                if self.current_row > 0:
                    self.current_row -= 1

            attempts += 1

    ###################################################
    # MANUAL MOVEMENT
    ###################################################

    def move_right(self):

        self.current_col += 1

        self.highlight_current_cell()

    def move_left(self):

        if self.current_col > 0:

            self.current_col -= 1

        self.highlight_current_cell()

    def move_down(self):

        self.current_row += 1

        self.highlight_current_cell()

    def move_up(self):

        if self.current_row > 0:

            self.current_row -= 1

        self.highlight_current_cell()

    ###################################################
    # HIGHLIGHT CURRENT CELL
    ###################################################

    def highlight_current_cell(self):

        try:

            controller = self.document.getCurrentController()

            cell = self.sheet.getCellByPosition(
                self.current_col,
                self.current_row
            )

            controller.select(cell)

        except Exception as e:

            print("Highlight error:", e)

    ###################################################
    # SETTINGS
    ###################################################

    def set_direction(self, direction):

        self.direction = direction

    def set_skip_filled(self, enabled):

        self.skip_filled = enabled

    ###################################################
    # POSITION
    ###################################################

    def get_position(self):

        return (
            self.current_row + 1,
            self.current_col + 1
        )

    ###################################################
    # POSITION STRING
    ###################################################

    def get_position_string(self):

        col_letter = chr(65 + self.current_col)

        return f"{col_letter}{self.current_row + 1}"