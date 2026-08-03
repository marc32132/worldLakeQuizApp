from django.test import TestCase
from django.urls import reverse
from lakes.models import Lake
from lakes.views import PAGE_SIZE

class TestLakesPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        Lake.objects.create(name="C Lake", country="England")
        Lake.objects.create(name="D Lake", country="Switzerland")
        Lake.objects.create(name="B Lake", country="Germany")
        Lake.objects.create(name="A Lake", country="Poland")

    def test_lakespage_status_code(self):
        '''Verify that the lakes list page loads successfully with a 200 OK status.'''

        response = self.client.get(reverse('lakes:list'))
        self.assertEqual(response.status_code, 200)

    def test_alphabetical_order_of_lakes_being_displayed(self):
        '''Verify that lakes are displayed in alphabetical order by default.'''

        response = self.client.get(reverse('lakes:list'))
        returned_names = [lake.name for lake in response.context["lakes"]]

        self.assertEqual(
            returned_names,
            ["A Lake", "B Lake", "C Lake", "D Lake"]
        )

    def test_correct_templates_used_for_htmx_and_normal_requests(self):
        '''Verify that the view returns the full page for standard requests and only the partial for htmx.'''

        # Normal request -> renders the main template (which includes the partial table)
        normal_response = self.client.get(reverse('lakes:list'))
        self.assertTemplateUsed(normal_response, 'lakes/lake_info.html')
        self.assertTemplateUsed(normal_response, 'lakes/partials/lake_table.html')

        # HTMX request -> renders ONLY the partial table, main template is untouched
        htmx_response = self.client.get(reverse('lakes:list'), HTTP_HX_REQUEST='true')
        self.assertTemplateUsed(htmx_response, 'lakes/partials/lake_table.html')
        self.assertTemplateNotUsed(htmx_response, 'lakes/lake_info.html')
        
    def test_htmx_search_returns_filtered_results(self):
        '''Verify that searching via HTMX returns only the matching lakes.'''

        response = self.client.get(reverse('lakes:list'), {'q': "Pol"}, HTTP_HX_REQUEST='true')
        returned_names = [lake.name for lake in response.context["lakes"]]

        self.assertEqual(returned_names, ["A Lake"])

    def test_htmx_search_no_results(self):
        '''Verify that searching for a non-existent phrase returns an empty list and a proper message.'''

        response = self.client.get(reverse('lakes:list'), {'q': "Roz"}, HTTP_HX_REQUEST='true')
        returned_names = [lake.name for lake in response.context["lakes"]]

        self.assertEqual(returned_names, [])
        self.assertContains(response, "No results found")

    def test_htmx_search_empty_query_returns_all_lakes(self):
        '''Verify that an empty search query resets the filter and returns all lakes in alphabetical order.'''

        response = self.client.get(reverse('lakes:list'), {'q': ""}, HTTP_HX_REQUEST='true')
        returned_names = [lake.name for lake in response.context["lakes"]]

        self.assertEqual(
            returned_names,
            ["A Lake", "B Lake", "C Lake", "D Lake"]
        )


    def test_pagination_returns_correct_number_of_items_per_page(self):
        '''Verify that pagination limits items to correct number, set with PAGE_SIZE, per page and splits content correctly.'''

        for i in range(PAGE_SIZE):
            Lake.objects.create(name=f"Extra Lake {i:02d}", country="Anywhere")

        response = self.client.get(reverse('lakes:list'))
        lakes_page = response.context["lakes"]

        # Verify page 1 has correct number of items and has a next page
        self.assertEqual(len(lakes_page), PAGE_SIZE)
        self.assertTrue(lakes_page.has_next())

        
        response_page_2 = self.client.get(reverse('lakes:list'), {'page': 2})
        lakes_page_2 = response_page_2.context["lakes"]

        # Verify page 2 has exactly 4 items and has a previous page
        self.assertEqual(len(lakes_page_2), 4)
        self.assertTrue(lakes_page_2.has_previous())

    def test_htmx_search_with_pagination_preserved(self):
        '''Verify that searching via HTMX preserves correct pagination behavior.'''

        for i in range(PAGE_SIZE+5):
            Lake.objects.create(name=f"Filtered Lake {i:02d}", country="Anywhere")

        # Request page 2 of the filtered HTMX search results
        response = self.client.get(
            reverse('lakes:list'), 
            {'q': 'Filtered', 'page': 2}, 
            HTTP_HX_REQUEST='true'
        )

        lakes_page = response.context["lakes"]

        # Verify page 2 has exactly 5 items and has a previous page
        self.assertEqual(len(lakes_page), 5)
        self.assertTrue(lakes_page.has_previous())

  
        # Verify that all items on page 2 actually match the search criteria
        returned_names = [lake.name for lake in lakes_page]
        for name in returned_names:
            self.assertIn("Filtered", name)