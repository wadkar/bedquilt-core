import testutils
import json
import string


class TestInsertDocument(testutils.BedquiltTestCase):

    def test_insert_into_non_existant_collection(self):
        doc = {
            "_id": "user@example.com",
            "name": "Some User",
            "age": 20
        }

        self.cur.execute("""
            select bq_insert_document('people', '{}');
        """.format(json.dumps(doc)))

        result = self.cur.fetchone()

        self.assertEqual(
            result, ('user@example.com',)
        )

        self.cur.execute("select bq_list_collections();")
        collections = self.cur.fetchall()
        self.assertIsNotNone(collections)

        self.assertEqual(collections, [("people",)])

    def test_insert_without_id(self):
        doc = {
            "name": "Some User",
            "age": 20
        }
        self.cur.execute("""
            select bq_insert_document('people', '{}');
        """.format(json.dumps(doc)))

        result = self.cur.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 1)

        _id = result[0]
        self.assertIn(type(_id), {str, unicode})
        self.assertEqual(len(_id), 24)
        for character in _id:
            self.assertIn(character, string.hexdigits)
