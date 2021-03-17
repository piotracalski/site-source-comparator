def get_number_of_images(markup):
  return len(markup.findAll('img'))


def compare_number_of_images(object):

  before_images_count = get_number_of_images(object.before_markup)
  after_images_count = get_number_of_images(object.after_markup)

  return before_images_count - after_images_count
  

def check_alt_attr(markup):

  images = markup.findAll('img')

  missing_alt_attr = 0
  empty_alt_attr = 0

  for image in images:
    try:
      image['alt']
    except:
      missing_alt_attr += 1
    else:
      if image['alt'] == '':
        empty_alt_attr += 1
  
  return {
    "missing_alt_attr": missing_alt_attr,
    "empty_alt_attr": empty_alt_attr
  }