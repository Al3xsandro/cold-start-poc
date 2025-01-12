document.addEventListener('DOMContentLoaded', function () {
  const emblaElements = document.querySelectorAll('.embla'); // Select all .embla elements

  emblaElements.forEach((rootNode) => {
    const viewportNode = rootNode.querySelector('.embla__viewport');
    const prevButtonNode = rootNode.querySelector('.embla__button--prev');
    const nextButtonNode = rootNode.querySelector('.embla__button--next');

    const embla = EmblaCarousel(viewportNode, {
      loop: true,
      draggable: true,
      speed: 1,
    });

    // Add event listeners for custom buttons
    prevButtonNode.addEventListener('click', () => embla.scrollPrev(), false);
    nextButtonNode.addEventListener('click', () => embla.scrollNext(), false);
  });
});