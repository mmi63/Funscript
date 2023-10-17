import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


def generate_md(filter, previous):

  # read from the spreadsheet
  scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name('funscript-4be905c4dda4.json', scope)
  gc = gspread.authorize(credentials)
  SPREADSHEET_KEY = '1CWxXCjYrvOH01FGGQX5wR-imdng848vw6HfxawA6oUI'
  worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

  # import data to pandas data frame
  data = worksheet.get_all_values()
  df = pd.DataFrame(data[1:], columns=data[0])
  df_filtered = df[df["description"] == filter]
  df_previous = df[df["description"] == previous]
  if df_filtered.empty:
    print('No entries found. Please check the filter condition.')
    exit()
  if df_previous.empty:
    print('No entries found. Please check the previous post information.')
    exit()

  # iwara monthly review article
  if 'iwara' in filter:
    print('Not equipped yet')

  # special feature article of a specific music
  else:
    f = open('../dance/' + filter + '.md', 'w', encoding='UTF-8')
    header = ['<!--⬇️ Thumbnail here ⬇️ -->\n', '\n',
              '<!--⬇️ Descriptions here ⬇️ -->\n', '\n', '\n',
              '**Song title:** ', df_filtered["music"].iloc[0], '\n',
              '**Artist:** ', df_filtered["artist"].iloc[0], '\n',
              '**BPM:** ', df_filtered["bpm"].iloc[0], '\n', '\n',
              'All scripts are made for and tested by Handy.\n',
              'The dance part is generated with the aid of [Funscript Dancer](https://discuss.eroscripts.com/t/funscriptdancer-generate-funscripts-from-music-beat-pitch-energy-cross-platform/73179) and [OpenFunscripter](https://discuss.eroscripts.com/t/openfunscripter-a-scripting-tool-3-2-0-release/87447).\n',
              '\n', 'Enjoy!\n', '\n', '**Template**\n',
              '<!--⬇️ Template funscript here ⬇️ -->\n', '\n',
              '<!--⬇️ Template heatmap here ⬇️ -->\n', '\n',
              '---\n', '\n']
    f.writelines(header)
    for category in ['Dance', 'Sex & Dance', 'Dance + Omake']:
      df_categorized = df_filtered[df_filtered["category"] == category]
      if not df_categorized.empty:
        f.write('[details="' + category + ': "]\n\n')
        for row in df_categorized.itertuples():
          content = [row.title, '\n',
                     '---', '\n', '\n',
                     '<!--⬇️ Thumbnail here ⬇️ -->\n', '\n',
                     'Creator: ', row.creator, '\n', '\n',
                     'Link: [', row.title, '](', row.link, ')\n', '\n',
                     'Script: ', '<!--⬇️ Script here ⬇️ -->\n', '\n', '\n']
          f.writelines(content)
        f.write('[/details]\n\n')
        f.write('---\n\n')
    footer = ['### :memo: Notes', '\n', '\n',
              'Let us know any recommendations of videos based on this song :slight_smile:', '\n', '\n',
              '|[⬅︎ previous: ', df_previous["music"].iloc[0], '](', df_previous["post"].iloc[0], ')|[next: ???]|', '\n',
              '|:--|--:|', '\n', '\n']
    f.writelines(footer)
