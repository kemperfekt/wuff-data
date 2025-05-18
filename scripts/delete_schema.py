from connect_weaviate import get_weaviate_client

def delete_schema():
    client = get_weaviate_client()
    classes = client.schema.get()["classes"]
    for c in classes:
        class_name = c["class"]
        print(f"Deleting class: {class_name}")
        client.schema.delete_class(class_name)

if __name__ == "__main__":
    delete_schema()