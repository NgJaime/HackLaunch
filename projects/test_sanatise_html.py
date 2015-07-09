from django.test import SimpleTestCase
from mock import MagicMock, patch
from projects.sanatise_html import clean_rich_html

class ClearRichHtmlTestCase(SimpleTestCase):

    def test_valid_iframe(self):
        input_text = '<iframe width="640" height="360" src="//www.youtube.com/embed/maj1iJlLz34" frameborder="0" allowfullscreen=""></iframe>'

        output_text = clean_rich_html(input_text)

        input_set = set(input_text[8:-10].split(' '))
        output_set = set(output_text[8:-10].split(' '))

        self.assertEqual(input_set, output_set)

    def test_invalid_iframe_src(self):
        input_text = '<iframe width="640" height="360" src="//www.danger.com/embed/maj1iJlLz34" frameborder="0" allowfullscreen=""></iframe>'

        output_text = clean_rich_html(input_text)

        input_set = set(input_text[8:-10].split(' '))
        output_set = set(output_text[8:-10].split(' '))

        difference = input_set - output_set

        self.assertEqual(difference, set(['src="//www.danger.com/embed/maj1iJlLz34"']))


    def test_invalid_script_src(self):
        input_text = '<script>console.log("danger")</script>'

        output_text = clean_rich_html(input_text)

        self.assertEqual(output_text, u'console.log("danger")')


    def test_invalid_event_trigger(self):
        input_text = '<img alt="Image title" src="data:image/jpeg;base64,/9j/4AAQSkZ" onclick="function() {console.log(danger);}">'

        output_text = clean_rich_html(input_text)

        self.assertEqual(output_text, u'<img alt="Image title" src="data:image/jpeg;base64,/9j/4AAQSkZ">')
