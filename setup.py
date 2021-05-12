from setuptools import setup, find_packages

setup(
    name="department_app",
    version="0.1",
    description="Application to perform CRUD operations on departments"
                "and employees via a REST-API.",
    author="Mark Onysko",
    author_email="argentumno3@gmail.com",
    url="https://github.com/MarkOnysko/epam_python_final_project",
    install_requires=[
        "Flask>=1.1.2",
        "Flask-Bootstrap>=3.3.7.1",
        "Flask-Migrate>=2.7.0",
        "Flask-SQLAlchemy>=2.5.1",
        "Flask-WTF>=0.14.3",
    ],
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
)
