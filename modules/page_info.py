def compare_page_title(object):
  
  titles = list()
  for markup in [object.before_markup, object.after_markup]:
    title_tag = markup.find('title')
    if title_tag:
      titles.append(title_tag.get_text())
    else:
      return 'No title tag'
      
  return titles[0] == titles[1]
  