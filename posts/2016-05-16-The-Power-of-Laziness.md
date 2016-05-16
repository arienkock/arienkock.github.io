---
title: The Power of Laziness
teaser: Lazily Concatenated Java 8 Streams
---

Lazy evaluation is a strong tool. With some effort it was always possible to use this in the Java language, but now it's easier than ever.

I was using streams to process structured data from a web API. They contained nested references to more data, and this could go on possibly infinitely.
 So, obviosuly memory was a constraint. Streams are already lazy, items are not fetched until necessary (except for some optimizations).
 However, there is no facility to concatenate streams lazily on demand. 

### Proposed solution 1: ###

```java
public class LazyConcat {
  public static <T> Stream<T> lazyConcat(
    Stream<T> first, 
    Supplier<Stream<T>> secondSupplier) {
    return Stream.of(() -> first, secondSupplier)
      .flatMap(Supplier::get);
  }
}
```

Here `flatMap` is effectively concatenating the two streams. The second stream is only created when the supplier's `get` method is called, and that only happens once the stream processing pipeline needs more items.

The second stream, once created, can itself be a lazy concatenation of two streams. As a result we could do this infinitely... were it not for the inevitable `StackOverflowError`.
So, even though this solution is lazy, it doesn't scale well.

### Proposed solution 2: ###

Conceptually, a trampoline is some code that invokes a function, and if that function returns a new function it invokes that one and repeats this process until the returned value is no longer a function.
This is a way to do recursion without actually consuming stack space. Invented here is the `StreamBounce`, which is a pointer to the current stream plus a way to get the next pointer.

`LazyConcat.trampoline` creates an iterator which returns all items in the current stream and advances the `StreamBounce` pointer until there is no "next" bounce.
The pointer is changed in place and there is no recursion. This solution can generate infinite streams.

```java
public class LazyConcat {
  public static <T> Stream<T> trampoline(
    Supplier<StreamBounce<T>> bouncer) {
    // Anonymous inner class doing all the work
    Iterator<? extends T> iterator = new Iterator<T>() {
      private Iterator<T> currentIterator = null;
      private StreamBounce currentBounce = null;
      
      // lazy init the firt stream on demand
      public Iterator<T> getCurrentIterator() {
        if (currentIterator == null) {
          currentBounce = bouncer.get();
          currentIterator = currentBounce.getCurrent().iterator();
        }
        return currentIterator;
      }

      // only return false if:
      //  - the current stream has no more elements
      //  - there is no next bounce
      public boolean hasNext() {
        if (!getCurrentIterator().hasNext()) {
          if (currentBounce != null) {
            // advance the pointer
            Supplier<StreamBounce> b = currentBounce.getNextBouncer();
            currentBounce = b == null ? null : b.get();
          }
          if (currentBounce == null) {
            return false;
          }
        }
        return true;
      }

      public T next() {
        if (!getCurrentIterator().hasNext() && currentBounce != null) {
          currentIterator = currentBounce.getCurrent().iterator();
        }
        return getCurrentIterator().next();
      }
    };
    // return stream built from the spliterator built from the iterator
    return StreamSupport.stream(
      Spliterators.spliteratorUnknownSize(
        iterator, 
        Spliterator.ORDERED), 
      false);
  }
}
```
    
```java    
public class StreamBounce <T> {
  private Stream<T> current;
  private Supplier<StreamBounce<T>> nextBouncer;
  ...
}
```

