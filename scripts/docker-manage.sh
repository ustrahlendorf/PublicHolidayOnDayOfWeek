#!/bin/bash
set -e

# Default values
ENVIRONMENT="development"

# Help message
show_help() {
    echo "Usage: $0 [OPTIONS] COMMAND"
    echo ""
    echo "Commands:"
    echo "  build       Build Docker images"
    echo "  up          Start containers"
    echo "  down        Stop containers"
    echo "  logs        Show container logs"
    echo "  test        Run tests"
    echo "  shell       Open a shell in the container"
    echo ""
    echo "Options:"
    echo "  -e, --env   Environment (development|production) [default: development]"
    echo "  -h, --help  Show this help message"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            COMMAND="$1"
            shift
            ;;
    esac
done

# Execute command
case $COMMAND in
    build)
        docker-compose build
        ;;
    up)
        docker-compose up -d
        ;;
    down)
        docker-compose down
        ;;
    logs)
        docker-compose logs -f
        ;;
    test)
        docker-compose run --rm app pytest
        ;;
    shell)
        docker-compose run --rm app /bin/bash
        ;;
    *)
        show_help
        exit 1
        ;;
esac 