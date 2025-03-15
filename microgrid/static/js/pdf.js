/* Source: https://www.geeksforgeeks.org/how-to-generate-pdf-file-using-jspdf-library/ */
async function convertHTMLtoPDF() {
    const { jsPDF } = window.jspdf;
    let doc = new jsPDF('p', 'in', [8.5, 11]);
    let pdfjs = document.querySelector('#divID');

    await doc.html(pdfjs, {
        html2canvas: {
            scale: 0.01 , // Adjust this value as needed
        },
        callback: function(doc) {
            doc.save("newpdf.pdf");
        },
        x: 1,
        y: 1
    });               
}; 

window.onload = function() { 
    let button = document.getElementById("button");
    button.addEventListener("click", function() {
        setTimeout(convertHTMLtoPDF, 1000); // delay of 1 second
    });          
};