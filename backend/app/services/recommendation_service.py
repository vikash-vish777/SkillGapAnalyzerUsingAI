from app.models.learning_resource import LearningResource

# Curated practical learning roadmaps for technical skills
SKILL_ROADMAPS = {
    "Docker": {
        "reason": "Containerization standardizes software environments, ensuring identical execution across development, staging, and production.",
        "topics": [
            "Container fundamentals and images vs containers",
            "Writing production-ready multi-stage Dockerfiles",
            "Managing persistent data with Docker Volumes",
            "Multi-container orchestration with Docker Compose",
            "Container networking and port binding",
            "Image security and minimizing attack surface",
        ],
        "practice_exercise": "Containerize a full-stack web application (React frontend + Flask API + MySQL database) with docker-compose.",
        "estimated_learning_time": "1 to 2 weeks",
    },
    "Kubernetes": {
        "reason": "De-facto industry standard for orchestrating, scaling, and managing containerized applications across cloud clusters.",
        "topics": [
            "Kubernetes architecture: Control Plane, Nodes, Kubelet",
            "Core manifests: Pods, Deployments, ReplicaSets",
            "Networking: ClusterIP, NodePort, Ingress controllers",
            "Configuration: ConfigMaps and Secrets management",
            "Persistent storage: PersistentVolumes and PVCs",
            "Health checks: Liveness and Readiness probes",
        ],
        "practice_exercise": "Deploy a multi-tier microservice cluster on local Minikube or Kind with an Ingress controller and auto-scaling.",
        "estimated_learning_time": "3 to 4 weeks",
    },
    "Python": {
        "reason": "Versatile, highly demanded language powering web backends, data engineering, AI/ML, and DevOps automation.",
        "topics": [
            "Python data structures, generators, and list comprehensions",
            "Object-Oriented Programming, classes, and inheritance",
            "Virtual environments and package management with pip",
            "Working with HTTP requests, JSON, and file streams",
            "Exception handling and logging best practices",
            "Unit testing with pytest",
        ],
        "practice_exercise": "Build a command-line utility or REST API that fetches and parses real-world JSON data with automated test coverage.",
        "estimated_learning_time": "2 to 3 weeks",
    },
    "React.js": {
        "reason": "Leading frontend library for creating dynamic, reactive, and component-based user interfaces.",
        "topics": [
            "JSX syntax, component lifecycle, and virtual DOM",
            "Hooks in depth: useState, useEffect, useRef, useMemo",
            "Custom hooks for reusable data fetching and state",
            "Client-side routing with React Router v6",
            "Global state management with Context API or Redux",
            "Performance optimization: React.memo and code splitting",
        ],
        "practice_exercise": "Build a responsive CRUD dashboard with interactive charts, pagination, and real-time form validations.",
        "estimated_learning_time": "2 to 3 weeks",
    },
    "Node.js": {
        "reason": "High-throughput asynchronous runtime allowing developers to write scalable server-side JavaScript.",
        "topics": [
            "Event Loop, non-blocking I/O, and asynchronous execution",
            "Core modules: fs, path, http, events, and stream",
            "Express.js framework: routing, middleware, and error handling",
            "JWT-based authentication and secure cookie handling",
            "Connecting to relational (MySQL) and NoSQL (MongoDB) databases",
            "API performance tuning and clustering",
        ],
        "practice_exercise": "Build a secured REST API with JWT authentication, rate limiting, and database persistence.",
        "estimated_learning_time": "2 to 3 weeks",
    },
    "Spring Boot": {
        "reason": "Enterprise enterprise standard for building reliable, production-ready Java microservices.",
        "topics": [
            "Dependency Injection and Inversion of Control (IoC)",
            "Building REST Controllers and mapping request bodies",
            "Spring Data JPA and Hibernate ORM integration",
            "Connecting Spring Boot applications to MySQL/PostgreSQL",
            "Security configuration with Spring Security and JWT",
            "Automated integration testing with MockMvc",
        ],
        "practice_exercise": "Build an e-commerce catalog API with Spring Boot, JPA entities, and database migrations.",
        "estimated_learning_time": "3 to 4 weeks",
    },
    "Machine Learning": {
        "reason": "Foundational discipline for building predictive models, classifications, and data-driven intelligence.",
        "topics": [
            "Supervised learning: Linear Regression, Logistic Regression, Decision Trees",
            "Unsupervised learning: K-Means clustering, PCA dimensionality reduction",
            "Data preprocessing: feature scaling, one-hot encoding, imputation",
            "Model evaluation: Precision, Recall, F1 Score, ROC-AUC, cross-validation",
            "Avoiding overfitting: Regularization (L1/L2) and hyperparameter tuning",
        ],
        "practice_exercise": "Train and evaluate a classifier on a real-world dataset to predict customer churn or price estimation.",
        "estimated_learning_time": "4 to 6 weeks",
    },
    "scikit-learn": {
        "reason": "Standard Python toolkit for implementing classical machine learning algorithms efficiently.",
        "topics": [
            "scikit-learn estimator, transformer, and predictor APIs",
            "Building robust data pipelines with Pipeline and ColumnTransformer",
            "Model selection with GridSearchCV and RandomizedSearchCV",
            "Text vectorization using CountVectorizer and TfidfVectorizer",
            "Model serialization and persistence with joblib",
        ],
        "practice_exercise": "Build an end-to-end scikit-learn pipeline for text classification or numerical prediction.",
        "estimated_learning_time": "2 weeks",
    },
    "MySQL": {
        "reason": "The most widely deployed open-source relational database in production web systems.",
        "topics": [
            "Relational modeling and Third Normal Form (3NF)",
            "Complex queries: INNER, LEFT, and FULL joins",
            "Aggregation, GROUP BY, and window functions",
            "Indexing strategies: B-tree indexes, compound keys, and EXPLAIN plans",
            "Transactions, ACID guarantees, and isolation levels",
        ],
        "practice_exercise": "Design a normalized database schema with foreign keys, indexes, and write complex reporting queries.",
        "estimated_learning_time": "1 to 2 weeks",
    },
    "REST APIs": {
        "reason": "Architectural standard for inter-service communication and web client-server data exchange.",
        "topics": [
            "HTTP methods semantics (GET, POST, PUT, PATCH, DELETE)",
            "Standard status codes and consistent error response formats",
            "Resource-oriented URI design and naming conventions",
            "Pagination, filtering, sorting, and versioning strategies",
            "API security: authentication, authorization, CORS, and rate limiting",
            "Testing and documenting endpoints with OpenAPI / Postman",
        ],
        "practice_exercise": "Design and document a complete RESTful API specification with OpenAPI/Swagger and test all endpoints.",
        "estimated_learning_time": "1 week",
    },
    "CI/CD": {
        "reason": "Automates testing and release workflows, reducing deployment risk and accelerating delivery.",
        "topics": [
            "Continuous Integration principles and automated test triggers",
            "Writing GitHub Actions workflows and YAML pipelines",
            "Building, tagging, and publishing Docker images to registries",
            "Automated linting, security audits, and code coverage checks",
            "Deployment strategies: Blue-Green and Rolling updates",
        ],
        "practice_exercise": "Create a GitHub Actions pipeline that lints code, runs unit tests, and builds a Docker image on every pull request.",
        "estimated_learning_time": "1 to 2 weeks",
    },
}

DEFAULT_ROADMAP = {
    "reason": "Essential competence required to fulfill industry standards for this job role.",
    "topics": [
        "Core concepts, syntax, and foundational architecture",
        "Best practices, design patterns, and anti-patterns",
        "Integration with modern application frameworks and databases",
        "Testing, debugging, and performance profiling",
    ],
    "practice_exercise": "Implement a focused hands-on mini-project demonstrating practical application of this technology.",
    "estimated_learning_time": "1 to 2 weeks",
}

class RecommendationService:
    """Generates structured, actionable learning recommendations for candidate skill gaps."""

    @classmethod
    def generate_recommendations(cls, missing_skills: list[dict]) -> list[dict]:
        """Builds tailored learning roadmaps with verified resources for each missing skill."""
        recommendations = []

        for skill_item in missing_skills:
            skill_name = skill_item["name"]
            skill_id = skill_item.get("skill_id")
            req_type = skill_item.get("requirement_type", "essential")
            priority = 1 if req_type == "essential" else 2

            roadmap_data = SKILL_ROADMAPS.get(skill_name, DEFAULT_ROADMAP)

            # Query verified learning resources from the database if skill_id exists
            verified_resources = []
            if skill_id:
                resources = LearningResource.query.filter_by(skill_id=skill_id).all()
                verified_resources = [res.to_dict() for res in resources]

            recommendations.append({
                "skill_name": skill_name,
                "skill_id": skill_id,
                "priority": priority,
                "importance_level": "High (Essential Requirement)" if priority == 1 else "Medium (Preferred Skill)",
                "reason": roadmap_data["reason"],
                "recommended_topics": roadmap_data["topics"],
                "practice_exercise": roadmap_data["practice_exercise"],
                "estimated_learning_time": roadmap_data["estimated_learning_time"],
                "resources": verified_resources,
                "completion_status": "pending",
            })

        # Sort recommendations: Priority 1 (Essential) first, then Priority 2 (Preferred)
        recommendations.sort(key=lambda r: (r["priority"], r["skill_name"]))
        return recommendations

