from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer


# =========================
# 📚 LIST + CREATE BOOKS
# =========================
@api_view(['GET', 'POST'])
def list_books(request):

    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()

        description = data.get("description", "")

        # 🔥 Smart Summary
        data["summary"] = description[:100] + "..." if len(description) > 100 else description

        # 🔥 Genre Detection
        desc = description.lower()

        if "habit" in desc or "productivity" in desc:
            genre = "Self-help"
        elif "money" in desc or "finance" in desc:
            genre = "Finance"
        elif "love" in desc or "story" in desc:
            genre = "Fiction"
        elif "business" in desc:
            genre = "Business"
        else:
            genre = "General"

        data["genre"] = genre

        serializer = BookSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Book added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# 📖 BOOK DETAIL
# =========================
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):

    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response(
            {"error": "Book not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(
            {"message": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# =========================
# 🤖 ASK QUESTION (FIXED)
# =========================
@api_view(['POST'])
def ask_question(request):

    question = request.data.get("question")

    if not question:
        return Response(
            {"error": "Question is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    question = question.lower()

    books = Book.objects.all()

    for book in books:
        if (
            book.title.lower() in question or
            book.genre.lower() in question
        ):
            return Response({
                "answer": f"Read '{book.title}' by {book.author}. It is a {book.genre} book."
            })

    return Response({
        "answer": "No exact match found, but explore our book collection!"
    })


# =========================
# 🎯 RECOMMENDATION ENGINE
# =========================
@api_view(['GET'])
def recommend_books(request, pk):

    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response(
            {"error": "Book not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    recommendations = Book.objects.filter(
        genre=book.genre
    ).exclude(id=book.id)

    serializer = BookSerializer(recommendations, many=True)

    return Response({
        "based_on": book.title,
        "recommendations": serializer.data
    })