import sys
import os

# Ensure backend directory is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app import create_app
from app.extensions import db
from app.models.job_role import JobRole
from app.models.skill import Skill
from app.models.job_required_skill import JobRequiredSkill
from app.models.learning_resource import LearningResource

# Curated Skills Data (Canonical names, normalized slugs, categories, descriptions)
SKILLS_DATA = [
    # Programming Languages
    {"name": "Python", "normalized": "python", "category": "Programming Language", "desc": "High-level programming language for web, scripting, and data science."},
    {"name": "JavaScript", "normalized": "javascript", "category": "Programming Language", "desc": "Dynamic scripting language for web client and server development."},
    {"name": "TypeScript", "normalized": "typescript", "category": "Programming Language", "desc": "Typed superset of JavaScript compiling to plain JavaScript."},
    {"name": "Java", "normalized": "java", "category": "Programming Language", "desc": "Object-oriented, class-based general-purpose programming language."},
    {"name": "SQL", "normalized": "sql", "category": "Programming Language", "desc": "Domain-specific language for managing relational databases."},
    {"name": "HTML5", "normalized": "html5", "category": "Frontend", "desc": "Standard markup language for documents designed to be displayed in a web browser."},
    {"name": "CSS3", "normalized": "css3", "category": "Frontend", "desc": "Style sheet language used for describing presentation of HTML documents."},
    
    # Frameworks & Libraries
    {"name": "React.js", "normalized": "react.js", "category": "Frontend", "desc": "Declarative component-based JavaScript library for building user interfaces."},
    {"name": "Node.js", "normalized": "node.js", "category": "Backend", "desc": "Asynchronous event-driven JavaScript runtime built on Chrome's V8 engine."},
    {"name": "Flask", "normalized": "flask", "category": "Backend", "desc": "Lightweight WSGI Python microframework for web applications and APIs."},
    {"name": "Django", "normalized": "django", "category": "Backend", "desc": "High-level Python web framework encouraging rapid, pragmatic development."},
    {"name": "Spring Boot", "normalized": "spring boot", "category": "Backend", "desc": "Open source Java framework used to build microservices and enterprise web apps."},
    {"name": "Redux", "normalized": "redux", "category": "Frontend", "desc": "Predictable state container for JavaScript applications."},

    # Databases & Storage
    {"name": "MySQL", "normalized": "mysql", "category": "Database", "desc": "Open-source relational database management system."},
    {"name": "PostgreSQL", "normalized": "postgresql", "category": "Database", "desc": "Powerful, open source object-relational database system."},
    {"name": "MongoDB", "normalized": "mongodb", "category": "Database", "desc": "Document-oriented NoSQL database for high volume data storage."},
    {"name": "Redis", "normalized": "redis", "category": "Database", "desc": "In-memory data structure store used as a database, cache, and message broker."},

    # Data Science & AI
    {"name": "Machine Learning", "normalized": "machine learning", "category": "Data Science & AI", "desc": "Study of algorithms that improve automatically through experience and data."},
    {"name": "scikit-learn", "normalized": "scikit-learn", "category": "Data Science & AI", "desc": "Machine learning library for the Python programming language."},
    {"name": "Pandas", "normalized": "pandas", "category": "Data Science & AI", "desc": "Fast, powerful, and flexible open source data analysis and manipulation tool."},
    {"name": "NumPy", "normalized": "numpy", "category": "Data Science & AI", "desc": "Fundamental package for scientific computing with Python arrays."},
    {"name": "Deep Learning", "normalized": "deep learning", "category": "Data Science & AI", "desc": "Subset of machine learning based on artificial neural networks."},
    {"name": "spaCy", "normalized": "spacy", "category": "Data Science & AI", "desc": "Industrial-strength natural language processing library in Python."},

    # DevOps & Cloud
    {"name": "Git", "normalized": "git", "category": "DevOps", "desc": "Distributed version control system for tracking changes in source code."},
    {"name": "Docker", "normalized": "docker", "category": "DevOps", "desc": "Platform to build, share, and run applications with containers."},
    {"name": "Kubernetes", "normalized": "kubernetes", "category": "DevOps", "desc": "Open-source system for automating deployment, scaling, and management of containerized apps."},
    {"name": "CI/CD", "normalized": "ci/cd", "category": "DevOps", "desc": "Continuous integration and continuous delivery/deployment practice."},
    {"name": "AWS", "normalized": "aws", "category": "Cloud", "desc": "Amazon Web Services comprehensive cloud computing platform."},
    {"name": "Linux", "normalized": "linux", "category": "DevOps", "desc": "Open-source Unix-like operating system kernel."},

    # Concepts & Soft Skills
    {"name": "REST APIs", "normalized": "rest apis", "category": "Architecture", "desc": "Representational State Transfer architectural style for networked web services."},
    {"name": "Agile Methodologies", "normalized": "agile methodologies", "category": "Process", "desc": "Iterative approach to project management and software development."},
]

# Verified Learning Resources
RESOURCES_DATA = {
    "React.js": [
        {"title": "Official React Documentation", "url": "https://react.dev/", "type": "documentation", "level": "beginner"},
        {"title": "Full Stack Open - React", "url": "https://fullstackopen.com/en/part1", "type": "course", "level": "intermediate"}
    ],
    "Docker": [
        {"title": "Docker Getting Started Guide", "url": "https://docs.docker.com/get-started/", "type": "documentation", "level": "beginner"},
        {"title": "Docker Curriculum", "url": "https://docker-curriculum.com/", "type": "tutorial", "level": "intermediate"}
    ],
    "Python": [
        {"title": "Official Python Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "documentation", "level": "beginner"},
        {"title": "Real Python Tutorials", "url": "https://realpython.com/", "type": "tutorial", "level": "intermediate"}
    ],
    "Spring Boot": [
        {"title": "Building a RESTful Web Service with Spring Boot", "url": "https://spring.io/guides/gs/rest-service/", "type": "tutorial", "level": "beginner"},
        {"title": "Spring Boot Reference Documentation", "url": "https://docs.spring.io/spring-boot/docs/current/reference/html/", "type": "documentation", "level": "intermediate"}
    ],
    "scikit-learn": [
        {"title": "scikit-learn User Guide", "url": "https://scikit-learn.org/stable/user_guide.html", "type": "documentation", "level": "intermediate"},
        {"title": "Machine Learning with Python and Scikit-Learn", "url": "https://realpython.com/tutorials/machine-learning/", "type": "tutorial", "level": "beginner"}
    ],
    "Kubernetes": [
        {"title": "Kubernetes Basics Tutorial", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "type": "documentation", "level": "intermediate"},
    ],
    "REST APIs": [
        {"title": "Architectural Styles and the Design of Network-based Software Architectures", "url": "https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm", "type": "documentation", "level": "advanced"},
        {"title": "RESTful API Design Best Practices", "url": "https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design", "type": "documentation", "level": "intermediate"}
    ]
}

# Standard Job Roles and Skill Profiles
JOB_ROLES_DATA = [
    {
        "title": "Full Stack Developer",
        "category": "Software Engineering",
        "description": "Designs and develops complete end-to-end web applications, integrating responsive frontends with scalable backend APIs and relational databases.",
        "skills": [
            ("React.js", 1.5, "essential"),
            ("JavaScript", 1.5, "essential"),
            ("Node.js", 1.2, "essential"),
            ("Python", 1.2, "essential"),
            ("REST APIs", 1.3, "essential"),
            ("MySQL", 1.2, "essential"),
            ("Git", 1.0, "essential"),
            ("HTML5", 1.0, "essential"),
            ("CSS3", 1.0, "essential"),
            ("Docker", 1.1, "preferred"),
            ("TypeScript", 1.1, "preferred"),
            ("CI/CD", 1.0, "preferred"),
        ]
    },
    {
        "title": "Frontend Engineer",
        "category": "Frontend",
        "description": "Specializes in building high-performance, accessible, responsive user interfaces and single page applications.",
        "skills": [
            ("React.js", 1.8, "essential"),
            ("JavaScript", 1.8, "essential"),
            ("HTML5", 1.5, "essential"),
            ("CSS3", 1.5, "essential"),
            ("TypeScript", 1.4, "essential"),
            ("Git", 1.0, "essential"),
            ("Redux", 1.2, "preferred"),
            ("REST APIs", 1.1, "preferred"),
        ]
    },
    {
        "title": "Backend Engineer",
        "category": "Backend",
        "description": "Focuses on server-side architecture, database schemas, microservice orchestration, performance optimization, and API reliability.",
        "skills": [
            ("Python", 1.6, "essential"),
            ("Flask", 1.4, "essential"),
            ("REST APIs", 1.6, "essential"),
            ("SQL", 1.5, "essential"),
            ("PostgreSQL", 1.4, "essential"),
            ("Git", 1.0, "essential"),
            ("Docker", 1.3, "essential"),
            ("Redis", 1.1, "preferred"),
            ("Linux", 1.1, "preferred"),
            ("CI/CD", 1.1, "preferred"),
        ]
    },
    {
        "title": "Data Scientist",
        "category": "Data Science & AI",
        "description": "Extracts insights from structured and unstructured data, formulates predictive statistical models, and builds machine learning pipelines.",
        "skills": [
            ("Python", 1.8, "essential"),
            ("Machine Learning", 1.8, "essential"),
            ("scikit-learn", 1.5, "essential"),
            ("Pandas", 1.6, "essential"),
            ("NumPy", 1.5, "essential"),
            ("SQL", 1.4, "essential"),
            ("Git", 1.0, "essential"),
            ("Deep Learning", 1.2, "preferred"),
            ("spaCy", 1.1, "preferred"),
        ]
    },
    {
        "title": "DevOps Engineer",
        "category": "Cloud & DevOps",
        "description": "Automates deployment pipelines, manages infrastructure as code, maintains container orchestrators, and ensures 99.9% system uptime.",
        "skills": [
            ("Docker", 1.8, "essential"),
            ("Kubernetes", 1.7, "essential"),
            ("Linux", 1.6, "essential"),
            ("CI/CD", 1.6, "essential"),
            ("Git", 1.2, "essential"),
            ("AWS", 1.5, "essential"),
            ("Python", 1.2, "preferred"),
            ("SQL", 1.0, "preferred"),
        ]
    }
]

def seed_database():
    """Initializes tables and populates canonical skills, job roles, and learning resources."""
    app = create_app()
    with app.app_context():
        print(f"[*] Ensuring all tables exist in database: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()

        # 1. Seed Skills
        skill_map = {}
        for skill_info in SKILLS_DATA:
            existing_skill = Skill.query.filter_by(normalized_name=skill_info["normalized"]).first()
            if not existing_skill:
                skill = Skill(
                    name=skill_info["name"],
                    normalized_name=skill_info["normalized"],
                    category=skill_info["category"],
                    description=skill_info["desc"],
                )
                db.session.add(skill)
                db.session.flush()
                skill_map[skill.name] = skill
                print(f"  + Added skill: {skill.name}")
            else:
                skill_map[existing_skill.name] = existing_skill

        db.session.commit()

        # 2. Seed Learning Resources
        for skill_name, resources in RESOURCES_DATA.items():
            skill = skill_map.get(skill_name)
            if not skill:
                continue
            for res_info in resources:
                existing_res = LearningResource.query.filter_by(
                    skill_id=skill.id,
                    resource_url=res_info["url"]
                ).first()
                if not existing_res:
                    res = LearningResource(
                        skill_id=skill.id,
                        title=res_info["title"],
                        resource_url=res_info["url"],
                        resource_type=res_info["type"],
                        difficulty_level=res_info["level"],
                    )
                    db.session.add(res)
                    print(f"  + Added resource for {skill_name}: {res_info['title']}")

        db.session.commit()

        # 3. Seed Job Roles & Required Skills
        for role_info in JOB_ROLES_DATA:
            existing_role = JobRole.query.filter_by(title=role_info["title"]).first()
            if not existing_role:
                role = JobRole(
                    title=role_info["title"],
                    category=role_info["category"],
                    description=role_info["description"],
                )
                db.session.add(role)
                db.session.flush()
                print(f"  + Added Job Role: {role.title}")
            else:
                role = existing_role

            for skill_name, weight, req_type in role_info["skills"]:
                skill = skill_map.get(skill_name)
                if not skill:
                    continue
                existing_req = JobRequiredSkill.query.filter_by(
                    job_role_id=role.id,
                    skill_id=skill.id
                ).first()
                if not existing_req:
                    req = JobRequiredSkill(
                        job_role_id=role.id,
                        skill_id=skill.id,
                        importance_weight=weight,
                        requirement_type=req_type,
                    )
                    db.session.add(req)

        db.session.commit()
        print("[*] Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
