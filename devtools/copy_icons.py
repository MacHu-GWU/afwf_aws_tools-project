# -*- coding: utf-8 -*-

"""
AWS publish icons for their services here https://aws.amazon.com/architecture/icons/.

1. click the "Asset Package" link and download the zip file to your local, and extract it. It should be a folder looks like "Asset-Package_{month}{day}{year}". The absolute path is for the ``asset_package_dir`` argument.
2. run this script, it will copy required icon file to ``afwf_aws_tools-project/icons`` folder, and create a ``icon_enum.py`` file.
3. copy the content of ``icon_enum.py`` file into the ``afwf_aws_tools-project/aws_tools/icons.__init__.py`` file.
4. re-run ``afwf_aws_tools-project/bin/build-wf.sh`` to copy the icons to the alfred workflow directory.
"""

from __future__ import print_function, unicode_literals
from pathlib_mate import Path

here = Path(__file__).parent
dir_project_root = here.parent
dir_icons = Path(dir_project_root, "icons")


def run(asset_package_dir):
    """
    Only need 64x64 or 48_light and .png file

    :param asset_package_dir:
    :return:
    """
    file_to_copy_dict = dict()
    for p in Path(asset_package_dir).select_file():
        if p.basename.endswith("_64.png") or p.basename.endswith("_48_Light.png"):
            file_to_copy_dict[p.fname] = p

    file_to_copy_list = [
        p
        for fname, p in sorted(file_to_copy_dict.items(), key=lambda x: x[0])
    ]
    for p in file_to_copy_list:
        p.copyto(new_dirpath=dir_icons)

    lines = [
        "class Icons:"
    ]
    lines.extend([
        "    {} = \"{}\"".format(
            p.basename \
                .replace("_64.png", "").replace("_48_Light.png", "") \
                .replace("-", "_").replace("_&_", "_"),
            p.basename,
        )
        for p in file_to_copy_list
    ])
    Path(here, "icon_enum.py").write_text("\n".join(lines))


if __name__ == "__main__":
    asset_package_dir = "/Users/sanhehu/Downloads/Asset-Package_09172021"
    run(asset_package_dir)
