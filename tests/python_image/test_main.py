import unittest
from unittest.mock import patch, mock_open, MagicMock

from python_image import main

class TestMain(unittest.TestCase):

    @patch('python_image.main.os.path.join', return_value='data/test.txt')
    @patch('python_image.main.os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_write_local_file(self, mock_file: MagicMock, mock_makedirs: MagicMock, mock_path_join: MagicMock) -> None:
        """
        Tests the write_local_file function.
        """
        main.write_local_file("test.txt", "test content")

        mock_makedirs.assert_called_once()
        mock_file.assert_called_once_with('data/test.txt', 'w')
        mock_file().write.assert_called_once_with('test content')

    @patch.dict('os.environ', {'GCP_BUCKET': 'test-bucket'})
    @patch('python_image.main.storage.Client')
    def test_write_to_gcs(self, mock_storage_client: MagicMock) -> None:
        """
        Tests the write_to_gcs function.
        """
        mock_blob = MagicMock()
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value.bucket.return_value = mock_bucket

        main.write_to_gcs('test_file.txt', 'test content')

        mock_storage_client.return_value.bucket.assert_called_once_with('test-bucket')
        mock_bucket.blob.assert_called_once_with('test_file.txt')
        mock_blob.upload_from_string.assert_called_once_with('test content')

    @patch('python_image.main.write_local_file')
    @patch('python_image.main.write_to_gcs')
    def test_main(self, mock_write_to_gcs: MagicMock, mock_write_local_file: MagicMock) -> None:
        """
        Tests the main function for both local and gcp environments.
        """
        # Test local environment
        with patch.dict('os.environ', {'ENVIRONMENT': 'local'}, clear=True):
            main.main()
            mock_write_local_file.assert_called_once_with("dummy_file.txt", "This is a dummy file.")
            mock_write_to_gcs.assert_not_called()

        mock_write_local_file.reset_mock()
        mock_write_to_gcs.reset_mock()

        # Test gcp environment
        with patch.dict('os.environ', {'ENVIRONMENT': 'gcp', 'GCS_BUCKET': 'test-bucket'}, clear=True):
            main.main()
            mock_write_to_gcs.assert_called_once_with("dummy_file.txt", "This is a dummy file.")
            mock_write_local_file.assert_not_called()
