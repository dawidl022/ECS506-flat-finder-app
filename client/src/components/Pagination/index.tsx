import React from "react";
import ReactPaginate from "react-paginate";

import styles from "./Pagination.module.scss";

interface PaginationProps {
  currentPage: number;
  setCurrentPage: (v: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  setCurrentPage,
}) => {
  const handlePageClick = (event: any) => {
    setCurrentPage(event.selected);
  };
  const pageCount = 10;
  return (
    <ReactPaginate
      className={styles.root}
      //   breakLabel="..."
      nextLabel=">"
      previousLabel="<"
      onPageChange={handlePageClick}
      pageRangeDisplayed={1}
      pageCount={pageCount}
      renderOnZeroPageCount={null}
      forcePage={currentPage}
    />
  );
};

export default Pagination;
