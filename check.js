/**************************************
 * Shift Manager API  (two-tab model)
 *  Sheet: employs   → A = user names      (roster)
 *  Sheet: users     → A = user | B = in | C = out  (shifts)
 **************************************/

// ---------- CONFIG ----------
const SS_ID       = '_';
const TAB_ROSTER  = 'employs';   // ← new roster tab
const TAB_SHIFTS  = 'users';     // ← existing shift log tab

// ---------- ENTRY ----------
function doGet() { return HtmlService.createHtmlOutputFromFile('index'); }

// ---------- MAIN ROUTER ----------
function handle(method, data) {
  const roster = SpreadsheetApp.openById(SS_ID).getSheetByName(TAB_ROSTER);
  const shifts = SpreadsheetApp.openById(SS_ID).getSheetByName(TAB_SHIFTS);

  switch (method) {

    /* ------- roster (column A on employs) ------------------------------ */
    case 'listUsers': {
      return roster
        .getRange(1, 1, roster.getLastRow())
        .getValues()
        .flat()
        .filter(String);                           // return array only
    }

    case 'addUser': {
      const name = (data.name || '').trim();
      if (!name) return { error: 'Missing name' };
      if (!hasUser(roster, name)) roster.appendRow([name]);
      return { status: 'added' };
    }

    case 'deleteUser': {
      const name = (data.name || '').trim();
      if (!name) return { error: 'Missing name' };
      const r = findRow(roster, name);
      if (r) roster.deleteRow(r);
      return { status: 'deleted' };
    }

    /* ------- clock-in / clock-out on users sheet ----------------------- */
    case 'clockIn':
    case 'clockOut': {
      const name = (data.name || '').trim();
      if (!name) return { error: 'Missing name' };

      const tz    = Session.getScriptTimeZone();
      const stamp = Utilities.formatDate(new Date(), tz, 'yyyy-MM-dd HH:mm:ss');

      if (method === 'clockIn') {
        shifts.appendRow([name, stamp, '']);
        return { status: 'clocked in', at: stamp };
      }

      const last = shifts.getLastRow();
      for (let r = last; r >= 1; r--) {
        const rowName = shifts.getRange(r, 1).getValue();
        const outVal  = shifts.getRange(r, 3).getValue();
        if (rowName === name && !outVal) {
          shifts.getRange(r, 3).setValue(stamp);
          return { status: 'clocked out', at: stamp };
        }
      }
      shifts.appendRow([name, '', stamp]);         // fallback
      return { status: 'clocked out (auto new row)', at: stamp };
    }

    default:
      return { error: 'Unknown method' };
  }
}

/* ---------- helpers (now use the sheet passed in) -------------------- */
function hasUser(sheet, name)  { return !!findRow(sheet, name); }
function findRow(sheet, name) {
  const vals = sheet.getRange('A:A').getValues();
  for (let i = 0; i < vals.length; i++) if (vals[i][0] === name) return i + 1;
  return null;
}

/* ---------- exported API for index.html ------------------------------ */
function listUsers()      { return handle('listUsers',  {}); }
function addUser(name)    { return handle('addUser',   { name }); }
function deleteUser(name) { return handle('deleteUser',{ name }); }
function clockIn(name)    { return handle('clockIn',   { name }); }
function clockOut(name)   { return handle('clockOut',  { name }); }
