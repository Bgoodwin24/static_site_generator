import os
import shutil
from gencontent import generate_pages_recursive
from copystatic import copy_files_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
	print("Deleting public directory...")
	if os.path.exists(dir_path_public):
		shutil.rmtree(dir_path_public)

	print("Copying static files to public directory...")
	copy_files_recursive(dir_path_static, dir_path_public)

	if not os.path.exists(template_path):
		print(f"Error: Template file not found at {template_path}")
		return
	
	if not os.path.exists(dir_path_content):
		print(f"Error: Content directory not found at {dir_path_content}")
		return
	
	print("Generating page...")
	generate_pages_recursive(dir_path_content, template_path, dir_path_public)

	print("Page generation complete!")

if __name__ == "__main__":
	main()